"""Embeddings of the test images and of synthetic noisy copies, with a disk cache (results/cache/<model>/)."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .clip import TINY, ImageEncoder, embed_arrays, embed_paths
from .config import ROOT, cache_dir
from .data import image_path, photos_table, read_rgb, test_set_of
from .noise import LEVELS as LIB_LEVELS
from .noise import NOISE_TYPES, TEST_SEED, make_noisy, seed_for

CACHED_MODEL = "openai/clip-vit-large-patch14"


def cached_frozen_test_features(m: pd.DataFrame):
    """The frozen ViT-L/14 features saved by the Step 2/fairness notebooks (Colab T4, fp16), in manifest order.
    Returns (V 840x768, T 33x768, label_keys)."""
    z = np.load(ROOT / "data" / "features" / "clip_vitl14_frozen.npz")
    idx = {im: i for i, im in enumerate(z["images"].astype(str))}
    V = z["V"][[idx[im] for im in m.image]]
    return V, z["T"], z["label_keys"].astype(str)


def test_embeddings(cfg: dict, m: pd.DataFrame, encoder: ImageEncoder | None, device, use_saved: bool = True):
    """Frozen-model embeddings of all 840 test images, in manifest order.

    use_saved and model == ViT-L/14 and the original test set -> the saved notebook features (instant, exactly
    the Step 2 numbers). Otherwise computed with `encoder` and cached in results/cache/<model>/test840.npz
    (another test set gets its own file, e.g. test840_recipe_b.npz, so the two never mix).
    """
    ts = test_set_of(m)
    if use_saved and cfg["model"] == CACHED_MODEL and ts == "original" and len(m) == 840:
        return cached_frozen_test_features(m)[0]
    name = f"test{len(m)}" + ("" if ts == "original" else f"_{ts}")       # e.g. test840, test960_recipe_b
    f = cache_dir(cfg) / f"{name}.npz"
    if f.exists() and cfg["model"] != TINY:
        z = np.load(f)
        if list(z["images"].astype(str)) == list(m.image):
            return z["V"]
    assert encoder is not None, "need the model to compute embeddings"
    V = embed_paths(encoder, [image_path(cfg, im) for im in m.image], device, cfg["batch_size"], desc="test images")
    if cfg["model"] != TINY:
        np.savez_compressed(f, images=m.image.to_numpy().astype(str), V=V)
    return V


def noisy_copies_table(m: pd.DataFrame, per_type: int, levels, seed: int) -> pd.DataFrame:
    """Which synthetic copies to make: every photo x every noise type x levels x per_type copies."""
    rows = []
    for p in photos_table(m).itertuples():
        for c in range(per_type):
            base = seed + c
            assert base != TEST_SEED, "noisy copies must not use the test set's seed family (299)"
            for t in NOISE_TYPES:
                for lv in levels:
                    rows.append((p.photo_id, p.disease, p.image, t, int(lv), c, seed_for(p.photo_id, t, int(lv), base)))
    return pd.DataFrame(rows, columns=["photo_id", "disease", "clean_image", "noise", "level", "copy", "seed"])


def noisy_copy_embeddings(cfg: dict, m: pd.DataFrame, encoder: ImageEncoder, device):
    """Frozen embeddings of the synthetic noisy copies of all 210 photos (cached). Returns (table, V)."""
    nc = cfg["noisy_copies"]
    tab = noisy_copies_table(m, int(nc["per_type"]), nc["levels"], int(nc["seed"]))
    lv = "".join(str(x) for x in nc["levels"])
    n_photos = tab.photo_id.nunique()
    extra = "" if n_photos == 210 else f"_p{n_photos}"                     # 240 photos with black gram
    f = cache_dir(cfg) / f"noisy_copies_seed{nc['seed']}_n{nc['per_type']}_L{lv}{extra}.npz"
    if f.exists() and cfg["model"] != TINY:
        z = np.load(f, allow_pickle=False)
        if len(z["V"]) == len(tab) and (z["seed"] == tab.seed.to_numpy()).all():
            return tab, z["V"]
    clean = {r.photo_id: read_rgb(image_path(cfg, r.image)) for r in photos_table(m).itertuples()}
    out, chunk = [], 512
    for i in range(0, len(tab), chunk):
        part = tab.iloc[i:i + chunk]
        arrays = [make_noisy(clean[r.photo_id], r.noise, r.level, r.seed) for r in part.itertuples()]
        out.append(embed_arrays(encoder, arrays, device, cfg["batch_size"]))
        print(f"  noisy copies: {min(i + chunk, len(tab))}/{len(tab)}", flush=True)
    V = np.concatenate(out)
    if cfg["model"] != TINY:
        np.savez_compressed(f, V=V, seed=tab.seed.to_numpy(), photo_id=tab.photo_id.to_numpy().astype(str))
    return tab, V


__all__ = ["test_embeddings", "noisy_copy_embeddings", "noisy_copies_table", "cached_frozen_test_features",
           "LIB_LEVELS"]
