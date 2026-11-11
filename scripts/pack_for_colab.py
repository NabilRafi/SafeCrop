"""Zip the code + small data (no images, no results) to dist/safecrop_code.zip for a Colab GPU run.

Upload that zip (and once, safecrop_test_images_840.zip) to your Google Drive folder (DRIVE_FOLDER_ID in the
notebook), then open notebooks/colab_gpu_runner.ipynb on a GPU runtime. See README.md, section 7.
The recipe-B images are left out too: run `python scripts/make_recipe_b.py` first on Colab to rebuild them
(it checks them against data/manifest_recipe_b.csv, which is in the zip).
"""
import _boot  # noqa: F401

import zipfile

from safecrop.config import ROOT

SKIP_DIRS = {"results", "dist", ".venv", "venv", ".git", "__pycache__", ".ipynb_checkpoints", ".mypy_cache"}
out = ROOT / "dist" / "safecrop_code.zip"
out.parent.mkdir(exist_ok=True)
n = 0
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for p in sorted(ROOT.rglob("*")):
        rel = p.relative_to(ROOT)
        if (p.is_dir() or set(rel.parts) & SKIP_DIRS or p.name == ".env"
                or rel.parts[:2] in {("data", "images"), ("data", "extra_references"),    # these come from the images zip
                                     ("data", "images_recipe_b")}):                       # rebuilt by make_recipe_b.py
            continue
        z.write(p, f"safecrop-clip-finetune/{rel.as_posix()}")
        n += 1
print(f"Wrote {out} ({n} files, {out.stat().st_size / 1e6:.1f} MB)")
