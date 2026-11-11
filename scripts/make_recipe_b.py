"""Build the recipe-B test set: the same 210 clean photos, noise types and folds, but L1-L3 made a
DIFFERENT way (src/safecrop/noise_b.py). Used to test whether methods that learned the test recipe's
noise (E1-E4) still work when the noise is made differently. No model is used here.

    python scripts/make_recipe_b.py --calibrate     # once: choose each noise type's strength per level
                                                     # (matched to the test set's average SSIM), paste
                                                     # the printed PARAMS into src/safecrop/noise_b.py
    python scripts/make_recipe_b.py                  # write data/images_recipe_b/ (630 images) + check

The first build also writes data/manifest_recipe_b.csv (840 rows: the 210 original clean photos + 630
recipe-B images, with a fingerprint of every image). Later builds (e.g. on Colab) never overwrite it:
they rebuild the images and report how many are identical to it.
Then score any method on it with --set test_set=recipe_b, for example:
    python scripts/noisy_database.py --set test_set=recipe_b --tag e1_rb
"""
import _boot  # noqa: F401

import hashlib
import math

import cv2
import numpy as np
import pandas as pd
from PIL import Image

from safecrop import noise_b
from safecrop.config import ROOT, cli, new_run_dir, path
from safecrop.data import BLACK_GRAM, RECIPE_B_PREFIX, image_path, load_manifest, read_rgb
from safecrop.noise import NICE, NOISE_TYPES, seed_for

MANIFEST_B = ROOT / "data" / "manifest_recipe_b.csv"


def fingerprint(img: np.ndarray) -> str:
    return hashlib.sha1(np.ascontiguousarray(img).tobytes()).hexdigest()[:16]


def clean_photos(cfg, m) -> dict:
    return {r.photo_id: read_rgb(image_path(cfg, r.image)) for r in m[m.level == "L0"].itertuples()}


def calibrate(cfg, m, run) -> None:
    """For each noise type and level: the knob whose average SSIM matches the test images' (same 42 photos)."""
    clean = clean_photos(cfg, m)
    rows, params = [], {}
    for noise in NOISE_TYPES:
        name, lo0, hi0, up, log = noise_b.KNOBS[noise]
        params[noise] = {}
        for lv in (1, 2, 3):
            sel = m[(m.noise == noise) & (m.level == f"L{lv}")]
            target = float(np.mean([noise_b.ssim(clean[r.photo_id], read_rgb(image_path(cfg, r.image)))
                                    for r in sel.itertuples()]))

            def score(k):
                return float(np.mean([noise_b.ssim(clean[p], noise_b.apply_b(
                    clean[p], noise, k, seed_for(p, noise, lv, noise_b.CALIBRATION_SEED))) for p in sel.photo_id]))

            lo, hi = lo0, hi0
            s_lo, s_hi = score(lo), score(hi)
            reachable = min(s_lo, s_hi) <= target <= max(s_lo, s_hi)
            best = (abs(s_lo - target), lo, s_lo) if abs(s_lo - target) < abs(s_hi - target) else (abs(s_hi - target), hi, s_hi)
            for _ in range(26):
                mid = math.sqrt(lo * hi) if log else (lo + hi) / 2
                s = score(mid)
                best = min(best, (abs(s - target), mid, s))
                if (s < target) == up:        # not enough damage yet? move towards more damage
                    lo = mid
                else:
                    hi = mid
                if best[0] < 0.0005:
                    break
            _, knob, got = best
            params[noise][lv] = float(f"{knob:.4g}")
            rows.append({"Noise": NICE[noise], "Level": f"L{lv}", "Knob": name, "Value": f"{knob:.4g}",
                         "SSIM test images": round(target, 3), "SSIM recipe B": round(got, 3),
                         "Reachable": "yes" if reachable else "NO (at the end of the range)"})
            print(f"  {noise:16} L{lv}: {name} = {knob:.4g}  SSIM {got:.3f} vs target {target:.3f}"
                  + ("" if reachable else "   <-- target outside the knob range"), flush=True)
    table = pd.DataFrame(rows)
    md = ["# Recipe B calibration", "",
          "Each knob is chosen so the average levelled colour MS-SSIM to the clean photo (multi-scale, per RGB channel, brightness and contrast matched first)",
          f"matches the test images' on the same 42 photos per noise type (calibration seeds {noise_b.CALIBRATION_SEED}).",
          "No model and no labels are used.", "", md_table(table), "", "Paste into src/safecrop/noise_b.py:", "",
          "```python", f"PARAMS = {params!r}", "```", ""]
    (run / "calibration.md").write_text("\n".join(md))
    print("\n".join(md[-4:]))
    print(f"\nSaved {run / 'calibration.md'}")


def md_table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    out += ["| " + " | ".join(str(v) for v in r) + " |" for r in df.itertuples(index=False)]
    return "\n".join(out)


def build(cfg, m, run) -> None:
    clean = clean_photos(cfg, m)
    out_dir = path(cfg["recipe_b_dir"])
    rows = []
    for r in m.itertuples():
        row = r._asdict()
        row.pop("Index")
        row["image"] = RECIPE_B_PREFIX + r.image
        row["test_set"] = "recipe_b"
        if r.level == "L0":                                  # the clean photos are the original files
            img, ssim_a, ssim_b = clean[r.photo_id], 1.0, 1.0
            row["severity"] = "clean"
        else:
            lv = int(r.level[1])
            img = noise_b.make_noisy_b(clean[r.photo_id], r.noise, lv, seed_for(r.photo_id, r.noise, lv, noise_b.RECIPE_B_SEED))
            f = out_dir / r.image
            f.parent.mkdir(parents=True, exist_ok=True)
            Image.fromarray(img).save(f)
            ssim_b = noise_b.ssim(clean[r.photo_id], img)
            ssim_a = noise_b.ssim(clean[r.photo_id], read_rgb(image_path(cfg, r.image)))
            row["severity"] = f"{noise_b.KNOBS[r.noise][0]}={noise_b.PARAMS[r.noise][lv]:g}"
        row.update(ssim_test_recipe=round(ssim_a, 4), ssim_recipe_b=round(ssim_b, 4), fingerprint=fingerprint(img))
        rows.append(row)
    b = pd.DataFrame(rows)
    print(f"Wrote {int((b.level != 'L0').sum())} recipe-B images to {out_dir}")

    noisy = b[b.level != "L0"]
    chk = noisy.groupby(["noise", "level"])[["ssim_test_recipe", "ssim_recipe_b"]].mean().round(3).reset_index()
    chk["noise"] = chk.noise.map(NICE)
    chk.columns = ["Noise", "Level", "SSIM test images", "SSIM recipe B"]
    lines = ["# Recipe B test set", "", f"{len(noisy)} noisy images (seed family {noise_b.RECIPE_B_SEED}) + the "
             f"{int((b.level == 'L0').sum())} original clean photos ({b.disease.nunique()} diseases).",
             "Average levelled colour MS-SSIM to the clean photo (multi-scale, per RGB channel, brightness and contrast matched first), test recipe vs recipe B:", "", md_table(chk), ""]

    if MANIFEST_B.exists():                                   # never overwrite the reference manifest
        ref = pd.read_csv(MANIFEST_B)
        same = b.merge(ref[["image", "fingerprint"]], on="image", suffixes=("", "_ref"))
        n_same = int((same.fingerprint == same.fingerprint_ref).sum())
        lines.append(f"Compared with data/manifest_recipe_b.csv: {n_same} of {len(ref)} images identical "
                     f"({len(same)} matched by name).")
        if n_same < len(ref):
            lines.append("Some images differ (usually a different WebP/OpenCV version); the CLIP scores use the "
                         "images built here.")
    else:
        b.to_csv(MANIFEST_B, index=False)
        lines.append(f"Wrote {MANIFEST_B.relative_to(ROOT)} ({len(b)} rows).")
    text = "\n".join(lines)
    (run / "summary.md").write_text(text + "\n")
    print(text)
    preview(cfg, m, b, run / "preview.png")


def preview(cfg, m, b, out_file) -> None:
    """One photo per noise type: clean | test recipe L1-L3 | recipe B L1-L3."""
    tiles = []
    for noise in NOISE_TYPES:
        pid = sorted(m[m.noise == noise].photo_id.unique())[0]
        row = [read_rgb(image_path(cfg, m[(m.photo_id == pid) & (m.level == "L0")].image.iloc[0]))]
        for d in (m, b):
            for lv in ("L1", "L2", "L3"):
                row.append(read_rgb(image_path(cfg, d[(d.photo_id == pid) & (d.level == lv)].image.iloc[0])))
        tiles.append(np.concatenate(row, 1))
    grid = np.concatenate(tiles, 0).copy()
    for i, t in enumerate(["clean", "test L1", "test L2", "test L3", "B L1", "B L2", "B L3"]):
        cv2.putText(grid, t, (i * 224 + 6, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 0), 2)
    Image.fromarray(grid).save(out_file)
    print(f"Preview: {out_file}")


def check(cfg, n: int = 30) -> int:
    """Quick check (smoke test): all recipe-B files exist and n random images rebuild identically. No writes."""
    if not MANIFEST_B.exists():
        print("data/manifest_recipe_b.csv is missing: run python scripts/make_recipe_b.py")
        return 1
    b = load_manifest({"test_set": "recipe_b", "black_gram": BLACK_GRAM in set(pd.read_csv(MANIFEST_B).disease)})
    noisy = b[b.level != "L0"]
    missing = [im for im in noisy.image if not image_path(cfg, im).exists()]
    if missing:
        print(f"{len(missing)} recipe-B images missing (e.g. {missing[0]}): run python scripts/make_recipe_b.py")
        return 1
    clean = clean_photos(cfg, b)
    same = 0
    for r in noisy.sample(n, random_state=0).itertuples():
        lv = int(r.level[1])
        img = noise_b.make_noisy_b(clean[r.photo_id], r.noise, lv, seed_for(r.photo_id, r.noise, lv, noise_b.RECIPE_B_SEED))
        same += fingerprint(img) == r.fingerprint and fingerprint(read_rgb(image_path(cfg, r.image))) == r.fingerprint
    print(f"recipe B: all {len(noisy)} images present; {same}/{n} random images rebuild identically")
    return 0 if same >= 0.9 * n else 1


if __name__ == "__main__":
    def extra(ap):
        ap.add_argument("--calibrate", action="store_true", help="choose the knobs (no images written)")
        ap.add_argument("--check", action="store_true", help="quick check of the existing images (no writes)")

    args, cfg = cli(__doc__, extra)
    if args.check:
        raise SystemExit(check(cfg))
    if args.calibrate:                                        # strengths are matched on the original 210 photos
        calibrate(cfg, load_manifest(), new_run_dir(cfg, "robustness", "recipe_b_calibration"))
    else:                                                     # build for black gram too, when it has been added
        with_bg = (ROOT / "data" / "manifest_black_gram.csv").exists()
        build(cfg, load_manifest({"black_gram": with_bg}), new_run_dir(cfg, "robustness", "recipe_b_build"))
