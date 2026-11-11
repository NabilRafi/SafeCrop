"""Add black gram yellow mosaic (the 8th disease) as an EXTENSION of the test set.

The 840 original images, data/manifest.csv and their folds stay exactly as they are. This script:
  1. copies the 120 black gram images (30 photos x L0-L3, 224 x 224 PNG) into data/images_black_gram/
     (a separate folder, so the frozen data/images/ is untouched and the images travel in the Colab code zip)
  2. checks every noisy image against our noise recipe (noise.py, test seeds 299): they must be rebuilt
     from their clean photo exactly (or within 1 grey level), like the other 630 noisy test images
  3. deals the 30 photos into the 5 folds, balanced by noise type (6 photos per fold; seeded shuffle, 299)
  4. writes data/manifest_black_gram.csv (120 rows, same columns as data/manifest.csv)

    python scripts/add_black_gram.py --source "../data/safecrop_test_images_840/images"

Then score with --set black_gram=true (8 diseases). Reports show the original 840 images (7 diseases)
and black gram separately.
"""
import _boot  # noqa: F401

import argparse
import random
import re
import shutil
from pathlib import Path

import numpy as np
import pandas as pd

from safecrop.config import ROOT, load_config, path
from safecrop.data import BLACK_GRAM, read_rgb
from safecrop.noise import NOISE_TYPES, make_noisy, seed_for

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--source", required=True, help="folder with L0..L3/black_gram_yellow_mosaic/*.png")
a = ap.parse_args()

cfg = load_config()
src, dst = Path(a.source).expanduser().resolve(), path(cfg["black_gram_dir"])
out_csv = ROOT / "data" / "manifest_black_gram.csv"
assert not out_csv.exists(), f"{out_csv} already exists: delete it first if you really want to rebuild it"
NAME = re.compile(rf"^{BLACK_GRAM}_(\d{{3}})_(clean|{'|'.join(NOISE_TYPES)})_L([0-3])\.png$")
SEVERITY = {1: 1, 2: 3, 3: 5}                         # library severity, as in data/manifest.csv (low light: 1/2/3)

rows = []
for lv in range(4):
    files = sorted((src / f"L{lv}" / BLACK_GRAM).glob("*.png"))
    assert len(files) == 30, f"expected 30 black gram images at L{lv}, found {len(files)} in {src / f'L{lv}' / BLACK_GRAM}"
    for f in files:
        mt = NAME.match(f.name)
        assert mt, f"unexpected file name {f.name}"
        num, noise, level = mt.group(1), mt.group(2), int(mt.group(3))
        assert (noise == "clean") == (level == 0), f"{f.name}: only L0 may be clean"
        img = read_rgb(f)
        assert img.shape == (224, 224, 3), f"{f.name} is {img.shape}, expected 224 x 224 x 3"
        rows.append({"file": f, "image": f"L{level}/{BLACK_GRAM}/{f.name}", "photo_id": f"{BLACK_GRAM}_{num}",
                     "noise": noise, "level": level})
df = pd.DataFrame(rows)

# each photo: one noise type at L1-L3 (and its L0 row gets the same noise type, like data/manifest.csv)
noise_of = df[df.level > 0].groupby("photo_id").noise.agg(lambda s: s.unique().tolist())
assert (noise_of.str.len() == 1).all(), "a photo has more than one noise type"
noise_of = noise_of.str[0]
assert set(noise_of.index) == set(df.photo_id) and len(noise_of) == 30
print("photos per noise type:", noise_of.value_counts().to_dict())
df["noise"] = df.photo_id.map(noise_of)

# 2. the noisy images must follow our recipe with the test seeds
clean = {r.photo_id: read_rgb(r.file) for r in df[df.level == 0].itertuples()}
diffs = []
for r in df[df.level > 0].itertuples():
    rebuilt = make_noisy(clean[r.photo_id], r.noise, r.level, seed_for(r.photo_id, r.noise, r.level))
    diffs.append(int(np.abs(rebuilt.astype(int) - read_rgb(r.file).astype(int)).max()))
diffs = np.array(diffs)
print(f"noise recipe check: {int((diffs == 0).sum())}/90 noisy images identical, "
      f"{int((diffs <= 1).sum())}/90 within 1 grey level, largest difference {diffs.max()}")
assert (diffs <= 1).all(), "some black gram images do not follow the test recipe (noise.py with seeds 299)"

# 3. folds: shuffle the 6 photos of each noise type (seed 299), deal them out in turn -> 6 photos per fold
rng = random.Random(299)
order = []
for t in NOISE_TYPES:
    ids = sorted(noise_of[noise_of == t].index)
    rng.shuffle(ids)
    order += ids
fold = {pid: i % 5 for i, pid in enumerate(order)}
df["fold"] = df.photo_id.map(fold)
print("photos per fold:", df[df.level == 0].fold.value_counts().sort_index().to_dict())

# 1 + 4. copy the images and write the manifest (same columns as data/manifest.csv)
for r in df.itertuples():
    t = dst / r.image
    t.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(r.file, t)
m = pd.DataFrame({
    "image": df.image, "photo_id": df.photo_id, "disease": BLACK_GRAM, "disease_name": "Black gram yellow mosaic",
    "group": "A", "origin": "Local", "noise": df.noise, "level": "L" + df.level.astype(str),
    "severity": [0 if lv == 0 else (lv if n == "low_light" else SEVERITY[lv]) for n, lv in zip(df.noise, df.level)],
    "fold": df.fold, "source_file": "IDBGL, Mendeley Data z55yrbmn2d (CC BY 4.0)"})
m = m.sort_values(["photo_id", "level"]).reset_index(drop=True)
m.to_csv(out_csv, index=False)
print(f"copied 120 images to {dst} and wrote {out_csv.relative_to(ROOT)} ({len(m)} rows)")
