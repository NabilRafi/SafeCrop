"""Step 0: is everything in place? Run this first on any new machine (takes ~30 s; no GPU needed).

    python scripts/check_setup.py               # environment, data, images, noise recipe, saved baseline
    python scripts/check_setup.py --load-model  # also downloads/loads CLIP and checks it matches the saved features
"""
import _boot  # noqa: F401
import random
import sys

import numpy as np
import pandas as pd

from safecrop.config import ROOT, cli, env_report
from safecrop.data import DISEASES, LEVELS, image_path, load_labels, load_manifest, missing_images, read_rgb
from safecrop.evaluate import BASELINES, database_vote, level_row, with_truth, zero_shot
from safecrop.features import CACHED_MODEL, cached_frozen_test_features
from safecrop.noise import make_noisy, seed_for

args, cfg = cli(__doc__, lambda ap: ap.add_argument("--load-model", action="store_true"))
problems = []


def ok(msg):
    print("  OK  ", msg)


def bad(msg):
    print("  FIX ", msg)
    problems.append(msg)


print("[1] Environment")
print("     ", env_report())
import torch  # noqa: E402
from safecrop.clip import pick_device  # noqa: E402
dev = pick_device(cfg["device"])
extra = f" ({torch.cuda.get_device_name(0)})" if dev.type == "cuda" else ""
ok(f"device: {dev}{extra}" + ("  <- fine for E0-E2; fine-tuning (E3) wants a GPU" if dev.type == "cpu" else ""))

print("[2] Data files")
m = load_manifest()
lab = load_labels()
p = m[m.level == "L0"]
ok(f"manifest: {len(m)} images, {m.photo_id.nunique()} photos, {len(DISEASES)} diseases, levels {sorted(m.level.unique())}")
ok(f"labels: {len(lab)} options ({int(lab.in_test_set.sum())} are test diseases)")
sizes = p.fold.value_counts().sort_index().tolist()
(ok if sizes == [42] * 5 else bad)(f"folds by photo: {sizes} photos per fold")
for name, f in BASELINES.items():
    (ok if (ROOT / "data" / "baselines" / f).exists() else bad)(f"baseline file {f}")

print("[3] Images")
miss = missing_images(cfg, m)
if miss:
    bad(f"{len(miss)} of 840 test images missing under {cfg['images_dir']}/ (e.g. {miss[0]}). "
        "Unzip safecrop_test_images_840.zip into data/images so you get data/images/L0, L1, L2, L3.")
else:
    ok(f"all 840 test images found in {cfg['images_dir']}/")
    shapes = {read_rgb(image_path(cfg, im)).shape for im in m.image.sample(20, random_state=0)}
    (ok if shapes == {(224, 224, 3)} else bad)(f"image size {shapes}")

    print("[4] Noise recipe (rebuild 25 random noisy test images from their clean L0 image)")
    l0 = dict(zip(p.photo_id, p.image))
    worst, exact = 0, 0
    for r in m[m.level != "L0"].sample(25, random_state=1).itertuples():
        lv = int(r.level[1])
        got = make_noisy(read_rgb(image_path(cfg, l0[r.photo_id])), r.noise, lv, seed_for(r.photo_id, r.noise, lv))
        d = int(np.abs(got.astype(int) - read_rgb(image_path(cfg, r.image)).astype(int)).max())
        worst, exact = max(worst, d), exact + (d == 0)
    (ok if worst <= 1 else bad)(f"{exact}/25 identical, largest difference {worst} grey level(s) (1 is normal for motion blur)")

print("[5] Saved frozen ViT-L/14 features -> Step 2 baseline")
V, T, keys = cached_frozen_test_features(m)
db = database_vote(V, m.photo_id, V[(m.level == "L0").to_numpy()], m.disease[m.level == "L0"].to_numpy(),
                   m.photo_id[m.level == "L0"].to_numpy(), cfg["database"]["k"])
zs = zero_shot(V, T, keys)
for name, out, f in [("CLIP database", db, "clip_database_7.csv"), ("CLIP zero-shot", zs, "clip_zero_shot_33.csv")]:
    old = pd.read_csv(ROOT / "data" / "baselines" / f).set_index("image").pred_label.reindex(m.image).to_numpy()
    same = int((old == out["pred"]).sum())
    r = level_row(with_truth(pd.DataFrame({"image": m.image, "pred_label": out["pred"]}), m))
    (ok if same == 840 else bad)(f"{name}: {same}/840 predictions identical to {f}; "
                                 + " / ".join(f"{lv} {r[lv]:.1f}" for lv in LEVELS) + f" / all {r['All']:.1f}")

if args.load_model:
    print(f"[6] Load {cfg['model']} and compare with the saved features")
    from safecrop.clip import ImageEncoder, embed_paths, load_clip
    enc = ImageEncoder(load_clip(cfg["model"])).to(dev).eval()
    if miss:
        bad("can't compare: images missing")
    else:
        idx = random.Random(0).sample(range(840), 8)
        E = embed_paths(enc, [image_path(cfg, m.image[i]) for i in idx], dev)
        if cfg["model"] == CACHED_MODEL:
            cos = (E * V[idx]).sum(1)
            (ok if cos.min() > 0.998 else bad)(f"cosine to saved features: min {cos.min():.5f} (> 0.998 expected)")
        else:
            ok(f"{cfg['model']} loaded; embeddings {E.shape} (no saved features to compare for this model)")

print()
if problems:
    print(f"{len(problems)} thing(s) to fix:")
    for x in problems:
        print("  -", x)
    sys.exit(1)
print("All checks passed. Next: python scripts/smoke_test.py, then see README.md section 6 (the experiments).")
