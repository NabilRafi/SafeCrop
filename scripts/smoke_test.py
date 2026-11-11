"""Runs every script once with a tiny RANDOM CLIP (configs/smoke.yaml): about 1-3 minutes on a laptop CPU.

Use it after changing code, before spending GPU time. It only checks that everything runs and writes
its files; the accuracy numbers of a random model mean nothing. Results go to results/_smoke/ (safe to delete).

    python scripts/smoke_test.py
"""
import _boot  # noqa: F401

import shutil
import subprocess
import sys
import time

from safecrop.config import ROOT

out = ROOT / "results" / "_smoke"
shutil.rmtree(out, ignore_errors=True)
runs = [
    ["scripts/check_setup.py"],
    ["scripts/reproduce_baseline.py", "--config", "configs/smoke.yaml", "--tag", "smoke"],
    ["scripts/noisy_database.py", "--config", "configs/smoke.yaml", "--tag", "smoke"],
    ["scripts/linear_probe.py", "--config", "configs/smoke.yaml", "--tag", "smoke"],
    ["scripts/finetune.py", "--config", "configs/smoke.yaml", "--tag", "smoke"],
    ["scripts/finetune.py", "--config", "configs/smoke.yaml", "--set", "finetune.epochs=0", "--tag", "smoke_e0"],
    ["scripts/finetune.py", "--config", "configs/smoke.yaml", "--set", "finetune.db_noisy_copies=true", "--tag", "smoke_db"],
    ["scripts/finetune.py", "--config", "configs/smoke.yaml", "--final", "--tag", "smoke_final"],
]
rb = (ROOT / "data" / "manifest_recipe_b.csv").exists()
if rb:                          # the recipe-B test set (robustness): images present and rebuildable, and scorable
    runs += [
        ["scripts/make_recipe_b.py", "--check", "--config", "configs/smoke.yaml"],
        ["scripts/noisy_database.py", "--config", "configs/smoke.yaml", "--set", "test_set=recipe_b", "--tag", "smoke_rb"],
        ["scripts/finetune.py", "--config", "configs/smoke.yaml", "--set", "test_set=recipe_b", "--tag", "smoke_rb"],
    ]
else:
    print("(recipe B not built yet: skipping its checks; run python scripts/make_recipe_b.py)")
bg = (ROOT / "data" / "manifest_black_gram.csv").exists()
if bg:                          # black gram as an 8th disease (and recipe B scored with the same trained models)
    runs += [
        ["scripts/reproduce_baseline.py", "--config", "configs/smoke.yaml", "--set", "black_gram=true", "--tag", "smoke_bg"],
        ["scripts/linear_probe.py", "--config", "configs/smoke.yaml", "--set", "black_gram=true", "--tag", "smoke_bg"],
        ["scripts/finetune.py", "--config", "configs/smoke.yaml", "--set", "black_gram=true",
         "--set", f"finetune.also_score_recipe_b={str(rb).lower()}", "--tag", "smoke_bg"],
    ]
failed = []


def run(r):
    t0 = time.time()
    p = subprocess.run([sys.executable, *r], cwd=ROOT, capture_output=True, text=True)
    status = "ok" if p.returncode == 0 else "FAILED"
    print(f"{status:6} {time.time() - t0:6.1f}s  python {' '.join(r)}")
    if p.returncode:
        failed.append(r)
        print(p.stdout[-2000:], p.stderr[-3000:], sep="\n")


for r in runs:
    run(r)
if bg and rb:                   # the robustness tables from one method scored on both test sets
    a_file = sorted(out.glob("finetune/*smoke_bg/predictions_database.csv"))
    b_file = sorted(out.glob("finetune/*smoke_bg_rb/predictions_database.csv"))
    if a_file and b_file:
        run(["scripts/robustness.py", "--method", "smoke", str(a_file[-1]), str(b_file[-1]),
             "--out", str(out / "robustness_smoke.md")])
expected = ["baseline/*/summary.md", "noisy_database/*/predictions_database.csv", "linear_probe/*/predictions_probe.csv",
            "finetune/*/predictions_database.csv", "finetune/*/predictions_head.csv", "finetune/*/neighbours.csv",
            "finetune_final/*/encoder_all_photos.pt", "runs.csv"]
if rb:
    expected += ["noisy_database/*smoke_rb/predictions_database.csv", "finetune/*smoke_rb/predictions_database.csv"]
if bg:
    expected += ["baseline/*smoke_bg/summary.md", "linear_probe/*smoke_bg/predictions_probe.csv",
                 "finetune/*smoke_bg/predictions_head.csv"]
if bg and rb:
    expected += ["finetune/*smoke_bg_rb/predictions_database.csv", "robustness_smoke.md"]
for pat in expected:
    if not list(out.glob(pat)):
        failed.append(pat)
        print("missing output:", pat)
print("\nSMOKE TEST", "PASSED" if not failed else f"FAILED ({len(failed)})")
sys.exit(1 if failed else 0)
