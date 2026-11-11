"""Compare any prediction files (columns: image, pred_label) with each other and with the Step 2 baselines.

    python scripts/compare.py results/finetune/<run>/predictions_database.csv
    python scripts/compare.py A.csv B.csv --names "fine-tuned" "noisy db" --out results/compare_A_B.md

Prints the slide tables (accuracy by level, A vs B, noise type) and McNemar head-to-heads against
the frozen CLIP database and Gemini + references (Step 2b), on the images all files share.
"""
import _boot  # noqa: F401

import argparse
from pathlib import Path

import pandas as pd

from safecrop.data import BLACK_GRAM, load_manifest
from safecrop.evaluate import BASELINES, MAIN_BASELINES, head_to_head, load_baselines, tables, with_truth

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("files", nargs="+")
ap.add_argument("--names", nargs="*", default=None)
ap.add_argument("--against", nargs="*", default=MAIN_BASELINES, choices=list(BASELINES),
                help="baselines for the head-to-head tests")
ap.add_argument("--out", default=None, help="also save the markdown here")
ap.add_argument("--test-set", default="original", choices=["original", "recipe_b"],
                help="the test set the files were scored on (recipe_b: no Step 2 / 2b baselines)")
ap.add_argument("--black-gram", action="store_true", help="the files include black gram (8 diseases)")
a = ap.parse_args()

m = load_manifest({"test_set": a.test_set, "black_gram": a.black_gram})
names = a.names or [Path(f).parent.name + "/" + Path(f).stem for f in a.files]
new = {n: with_truth(pd.read_csv(f, keep_default_na=False)[["image", "pred_label"]], m) for n, f in zip(names, a.files)}
common = set.intersection(*[set(d.image) for d in new.values()])
new = {n: d[d.image.isin(common)] for n, d in new.items()}
base = {} if a.test_set != "original" else {k: v[v.image.isin(common)] for k, v in load_baselines(m).items()}
old = {n: d[d.disease != BLACK_GRAM] for n, d in new.items()}          # the 840 original images
md = [f"Images compared: {len(common)} of {len(m)} (test set: {a.test_set}{'; 8 diseases' if a.black_gram else ''})",
      "", "## The original images (7 diseases)" if a.black_gram else "", tables({**old, **base}),
      head_to_head(old, {k: v for k, v in base.items() if k in a.against})]
if a.black_gram:
    md += ["## Black gram yellow mosaic only", "", tables({n: d[d.disease == BLACK_GRAM] for n, d in new.items()})]
if len(new) == 2:
    (n1, d1), (n2, d2) = new.items()
    md.append(head_to_head({n1: d1}, {n2: d2}))
text = "\n".join(md)
print(text)
if a.out:
    Path(a.out).write_text(text)
    print(f"\nSaved {a.out}")
