"""Robustness test: does each method still work when the noise is made a different way (recipe B)?

Give each method twice: its predictions on the original test images and on the recipe-B images
(same photos, noise types, levels and folds; only the noise recipe differs, see src/safecrop/noise_b.py).

    python scripts/robustness.py \\
        --method "E0 frozen database" results/baseline/<run>/predictions_database.csv results/baseline/<run_rb>/predictions_database.csv \\
        --method "E1 frozen + noisy copies" results/noisy_database/<run>/predictions_database.csv results/noisy_database/<run_rb>/predictions_database.csv \\
        --out results/robustness_<date>.md

Writes: accuracy by level (test recipe vs recipe B), the drop with a paired McNemar test (the same photo
at the same level, made with the two recipes), the usual slide tables on recipe B, and head-to-head
McNemar tests between the methods on recipe B. Only images every file shares are used.
"""
import _boot  # noqa: F401

import argparse
from itertools import combinations
from pathlib import Path

import pandas as pd

from safecrop.data import BLACK_GRAM, RECIPE_B_PREFIX, load_manifest
from safecrop.evaluate import fmt_p, level_row, mcnemar, md_table, tables, with_truth

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--method", nargs=3, action="append", required=True, metavar=("NAME", "ORIGINAL_CSV", "RECIPE_B_CSV"))
ap.add_argument("--out", default=None, help="also save the markdown here (never overwrites)")
a = ap.parse_args()

files = [f for _, fa, fb in a.method for f in (fa, fb)]
with_bg = any(pd.read_csv(f, usecols=["image"]).image.str.contains(f"/{BLACK_GRAM}/").any() for f in files)
m_a = load_manifest({"black_gram": with_bg})
m_b = load_manifest({"test_set": "recipe_b", "black_gram": with_bg})


def read(f, m):
    return with_truth(pd.read_csv(f, keep_default_na=False)[["image", "pred_label"]], m)


orig = {n: read(fa, m_a) for n, fa, _ in a.method}
recb = {n: read(fb, m_b) for n, _, fb in a.method}
for n, d in recb.items():                      # recipe-B names -> the original names (same photo and level)
    d["image"] = d.image.str.replace(RECIPE_B_PREFIX, "", n=1, regex=False)
common = set.intersection(*[set(d.image) for d in [*orig.values(), *recb.values()]])
orig = {n: d[d.image.isin(common)].reset_index(drop=True) for n, d in orig.items()}
recb = {n: d[d.image.isin(common)].reset_index(drop=True) for n, d in recb.items()}

md = ["# Robustness: test recipe vs recipe B (noise made a different way)", "",
      f"Images compared: {len(common)} of {len(m_a)} per test set (only images that every file scored).",
      "Recipe B: same photos, noise types, levels and folds; each level matched to the test images' damage "
      "(levelled colour MS-SSIM). Every method learned or built its references from the TEST recipe's noise only.", ""]

subsets = [("7 diseases", lambda d: d[d.disease != BLACK_GRAM]), ("black gram", lambda d: d[d.disease == BLACK_GRAM])] \
    if with_bg else [("", lambda d: d)]
rows = []
for n in orig:
    for sub, pick in subsets:
        da, db = pick(orig[n]), pick(recb[n])
        ra, rb = level_row(da), level_row(db)
        for lv in ["L3", None]:
            t = mcnemar(db, da, lv)             # only right on recipe B vs only right on the test recipe
            rows.append({"Method": n + (f" ({sub})" if sub else ""), "Levels": lv or "All",
                         "Test recipe %": ra[lv or "All"], "Recipe B %": rb[lv or "All"],
                         "Change": round(rb[lv or "All"] - ra[lv or "All"], 1), "Images": t["images"],
                         "Only B right": t["only_new_right"], "Only test right": t["only_baseline_right"],
                         "p": fmt_p(t["p"])})
md += ["## Accuracy drop from the test recipe to recipe B (paired McNemar: same photo, same level)", "",
       md_table(rows, "Method"), ""]

for sub, pick in subsets:
    title = f" ({sub})" if sub else ""
    md += [f"## Recipe B{title}: the usual tables", "", tables({f"{n} [recipe B]": pick(d) for n, d in recb.items()})]
    md += [f"## Test recipe{title}, same images: the usual tables", "",
           tables({f"{n} [test recipe]": pick(d) for n, d in orig.items()})]

if len(recb) > 1:
    for sub, pick in subsets:
        rows = []
        for x, y in combinations(list(recb), 2):
            for lv in ["L3", None]:
                t = mcnemar(pick(recb[x]), pick(recb[y]), lv)
                rows.append({"Method A": x, "Method B": y, "Levels": lv or "All", "Images": t["images"],
                             "Only A right": t["only_new_right"], "Only B right": t["only_baseline_right"],
                             "p": fmt_p(t["p"])})
        md += [f"## Methods against each other on recipe B{f' ({sub})' if sub else ''} (McNemar)", "",
               md_table(rows, "Method A"), ""]

text = "\n".join(md)
print(text)
if a.out:
    out = Path(a.out)
    assert not out.exists(), f"{out} exists: results are never overwritten"
    out.write_text(text)
    print(f"\nSaved {out}")
