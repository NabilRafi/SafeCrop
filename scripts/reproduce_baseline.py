"""E0: frozen CLIP on all 840 images -> CLIP photo database + zero-shot, scored like Step 2.

With ViT-L/14 this recomputes the embeddings from the images (it does NOT use the saved features)
and should give the Step 2 numbers: database 100 / 93.3 / 71.9 / 40.0 (all 76.3), zero-shot
25.7 / 15.2 / 8.6 / 3.8. A few predictions may flip on another GPU/CPU (fp16 vs fp32 rounding).
With another model (e.g. --config configs/vitb16_fast.yaml) this IS that model's frozen baseline.

    python scripts/reproduce_baseline.py
    python scripts/reproduce_baseline.py --config configs/vitb16_fast.yaml
"""
import _boot  # noqa: F401

import pandas as pd

from safecrop.clip import TINY, ImageEncoder, load_clip, load_tokenizer, pick_device, text_vectors
from safecrop.config import ROOT, cli, new_run_dir
from safecrop.data import load_labels, load_manifest, missing_images
from safecrop.evaluate import (database_vote, predictions_frame, reference_hits, with_truth, write_report,
                               zero_shot)
from safecrop.features import test_embeddings

args, cfg = cli(__doc__)
m, lab = load_manifest(cfg), load_labels()
assert not missing_images(cfg, m), "test images missing: run scripts/check_setup.py"
dev = pick_device(cfg["device"])
print(f"Loading {cfg['model']} on {dev} ...")
clip = load_clip(cfg["model"])
enc = ImageEncoder(clip).to(dev).eval()
V = test_embeddings(cfg, m, enc, dev, use_saved=False)

run = new_run_dir(cfg, "baseline", args.tag)
L0 = (m.level == "L0").to_numpy()
db = database_vote(V, m.photo_id, V[L0], m.disease[L0].to_numpy(), m.photo_id[L0].to_numpy(), cfg["database"]["k"])
name_db = f"CLIP database, frozen {cfg['model'].split('/')[-1]} (recomputed)"
pdb = predictions_frame(m.image, name_db, db)
pdb.to_csv(run / "predictions_database.csv", index=False)
ref_images = m.image[L0].to_numpy()
pd.DataFrame([(m.image[i], r + 1, ref_images[j], db["nearest_labels"][i, r], round(float(db["similarity"][i, r]), 4),
               cfg["model"]) for i in range(len(m)) for r, j in enumerate(db["nearest"][i])],
             columns=["image", "rank", "ref_image", "ref_disease", "similarity", "clip_model"]
             ).to_csv(run / "neighbours.csv", index=False)
new = {name_db: with_truth(pdb, m)}
notes = [f"model {cfg['model']}, k = {cfg['database']['k']}, leave-one-photo-out, {m.disease.nunique()} diseases"]

if cfg["model"] != TINY:
    T = text_vectors(clip.to(dev), load_tokenizer(cfg["model"]), lab, dev)
    scale = float(clip.logit_scale.exp().item())
    zs = zero_shot(V, T, lab.key.to_numpy(), scale)
    name_zs = f"CLIP zero-shot, frozen {cfg['model'].split('/')[-1]} (recomputed)"
    pzs = predictions_frame(m.image, name_zs, zs)
    pzs.to_csv(run / "predictions_zero_shot.csv", index=False)
    new[name_zs] = with_truth(pzs, m)

for f, (n, df) in zip(["clip_database_7.csv", "clip_zero_shot_33.csv"], new.items()):
    if cfg["test_set"] != "original":        # the saved Step 2 files are for the original images only
        break
    d = df[df.image.isin(set(load_manifest().image))]                   # the 840 original images
    old = pd.read_csv(ROOT / "data" / "baselines" / f).set_index("image").pred_label.reindex(d.image)
    notes.append(f"{n}: {int((old.to_numpy() == d.pred_label.to_numpy()).sum())}/840 predictions identical to "
                 f"the saved Step 2 file {f}" + (" (black gram is an extra choice here)" if len(d) < len(df) else ""))

text = write_report(run, "E0: frozen CLIP baseline", new, m, notes,
                    extra_md=reference_hits(new[name_db], db["nearest_labels"]))
print(text)
print(f"\nSaved in {run}")
