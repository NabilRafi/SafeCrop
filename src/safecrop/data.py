"""The 840-image test set: manifest, labels, folds, image loading and the training dataset."""
from __future__ import annotations

import random
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

from .config import ROOT, path
from .noise import random_noisy

DISEASES = ["apple_scab", "potato_late_blight", "rice_stem_borer",                      # group A, info-rich
            "grape_leaf_blight", "pear_leaf_spot", "jute_mosaic", "jute_dieback"]      # group B, info-scarce
BLACK_GRAM = "black_gram_yellow_mosaic"         # the 8th disease (group A, Local), an extension added 11 Nov
ALL_DISEASES = DISEASES + [BLACK_GRAM]
GROUP = {**{d: ("A" if i < 3 else "B") for i, d in enumerate(DISEASES)}, BLACK_GRAM: "A"}
LEVELS = ["L0", "L1", "L2", "L3"]
TEST_SETS = ("original", "recipe_b")
RECIPE_B_PREFIX = "recipe_b/"      # recipe-B image names start with this, so they never clash with the 840


def load_manifest(cfg: dict | None = None) -> pd.DataFrame:
    """One row per test image: image (relative path), photo_id, disease, group (A/B), noise, level, fold, ...

    cfg["test_set"] picks the test set: "original" (default: data/manifest.csv, the 840 images) or
    "recipe_b" (data/manifest_recipe_b.csv from scripts/make_recipe_b.py: the same clean photos,
    noise types and folds, with L1-L3 made by a different noise recipe).
    cfg["black_gram"] = True adds the 8th disease (data/manifest_black_gram.csv: 30 photos, 120 images, with
    their own folds; from scripts/add_black_gram.py). The 840 original rows and their folds never change.
    """
    cfg = cfg or {}
    test_set, with_bg = cfg.get("test_set", "original"), bool(cfg.get("black_gram", False))
    if test_set not in TEST_SETS:
        raise ValueError(f"test_set must be one of {TEST_SETS}, got {test_set!r}")
    m = pd.read_csv(ROOT / "data" / "manifest.csv")
    assert len(m) == 840 and m.image.is_unique, "data/manifest.csv should list 840 different images"
    assert set(m.disease) == set(DISEASES)
    if with_bg:
        f = ROOT / "data" / "manifest_black_gram.csv"
        assert f.exists(), "data/manifest_black_gram.csv is missing: run python scripts/add_black_gram.py"
        g = pd.read_csv(f)
        assert len(g) == 120 and set(g.disease) == {BLACK_GRAM}, "manifest_black_gram.csv should list 120 images"
        m = pd.concat([m, g], ignore_index=True)
        assert len(m) == 960 and m.image.is_unique
    if test_set == "original":
        return m
    f = ROOT / "data" / "manifest_recipe_b.csv"
    assert f.exists(), "data/manifest_recipe_b.csv is missing: run python scripts/make_recipe_b.py"
    b = pd.read_csv(f)
    assert b.image.is_unique and b.image.str.startswith(RECIPE_B_PREFIX).all()
    if not with_bg:
        b = b[b.disease != BLACK_GRAM].reset_index(drop=True)
    key = ["photo_id", "level", "disease", "group", "noise", "fold"]
    assert len(b) == len(m) and len(b[key].merge(m[key], on=key)) == len(m), (
        "recipe B must cover the same photos, noise types and folds (with black gram: rebuild it with "
        "python scripts/make_recipe_b.py after scripts/add_black_gram.py)")
    return b


def disease_list(m: pd.DataFrame) -> list[str]:
    """The classes a model chooses from: the 7 diseases, plus black gram when the manifest has it."""
    present = set(m.disease)
    return [d for d in ALL_DISEASES if d in present]


def test_set_of(m: pd.DataFrame) -> str:
    """Which test set a manifest (or a predictions table merged with it) belongs to."""
    return str(m["test_set"].iloc[0]) if "test_set" in m.columns and len(m) else "original"


def load_labels() -> pd.DataFrame:
    """The 33 options used by CLIP zero-shot and Gemini (7 test diseases + look-alikes + healthy)."""
    lab = pd.read_csv(ROOT / "data" / "labels.csv")
    assert len(lab) == 33
    return lab


def image_path(cfg: dict, image: str) -> Path:
    """Where a test image lives. Recipe-B names ('recipe_b/L3/...') point into cfg['recipe_b_dir'],
    except their clean L0 photos, which are the original files."""
    if image.startswith(RECIPE_B_PREFIX):
        rest = image[len(RECIPE_B_PREFIX):]
        if not rest.startswith("L0/"):
            return path(cfg.get("recipe_b_dir", "data/images_recipe_b")) / rest
        image = rest
    if image.split("/")[1:2] == [BLACK_GRAM]:            # the black gram extension has its own folder
        return path(cfg.get("black_gram_dir", "data/images_black_gram")) / image
    return path(cfg["images_dir"]) / image


def missing_images(cfg: dict, m: pd.DataFrame | None = None) -> list[str]:
    m = load_manifest(cfg) if m is None else m
    return [im for im in m.image if not image_path(cfg, im).exists()]


def read_rgb(p) -> np.ndarray:
    return np.array(Image.open(p).convert("RGB"))


def photos_table(m: pd.DataFrame) -> pd.DataFrame:
    """One row per photo (its clean L0 image), in manifest order."""
    return m[m.level == "L0"].reset_index(drop=True)


def fold_photos(m: pd.DataFrame, fold: int) -> tuple[list[str], list[str]]:
    """(training photo_ids, held-out photo_ids) for one of the 5 fixed folds in data/manifest.csv."""
    p = photos_table(m)
    return p[p.fold != fold].photo_id.tolist(), p[p.fold == fold].photo_id.tolist()


def geometric(img: np.ndarray, rng: random.Random) -> np.ndarray:
    """Random flip and quarter turn: a leaf photo has no fixed 'up'."""
    if rng.random() < 0.5:
        img = img[:, ::-1]
    return np.ascontiguousarray(np.rot90(img, rng.randrange(4)))


class PairDataset:
    """Training items for fine-tuning: (clean view, noisy view(s), disease index) for each training photo.

    Only CLEAN L0 images of training photos are read; the noisy views are made on the fly with
    random noise types/levels and fresh seeds, never the fixed test files. Call ``set_epoch``
    before each epoch so the noise differs between epochs but is reproducible.
    """

    def __init__(self, cfg: dict, m: pd.DataFrame, photo_ids: list[str], seed: int,
                 noisy_views: int = 1, geometric_aug: bool = True, levels=(1, 2, 3)):
        p = photos_table(m).set_index("photo_id").loc[photo_ids].reset_index()
        self.photo_ids = list(p.photo_id)
        classes = disease_list(m)
        self.labels = [classes.index(d) for d in p.disease]
        self.images = [read_rgb(image_path(cfg, im)) for im in p.image]     # 224 x 224 x 3 uint8
        self.seed, self.noisy_views, self.geo, self.levels = seed, noisy_views, geometric_aug, tuple(levels)
        self.epoch = 0

    def set_epoch(self, epoch: int) -> None:
        self.epoch = epoch

    def __len__(self) -> int:
        return len(self.images)

    def __getitem__(self, i: int):
        rng = random.Random(f"{self.seed}/{self.epoch}/{self.photo_ids[i]}")
        img = self.images[i]
        clean = geometric(img, rng) if self.geo else img
        noisy = [random_noisy(clean, rng, levels=self.levels)[0] for _ in range(self.noisy_views)]
        return np.stack([clean] + noisy), self.labels[i]


def collate_pairs(batch):
    """-> uint8 array (B, 1 + noisy_views, H, W, 3) and int labels (B,)."""
    x = np.stack([b[0] for b in batch])
    y = np.array([b[1] for b in batch], dtype=np.int64)
    return x, y
