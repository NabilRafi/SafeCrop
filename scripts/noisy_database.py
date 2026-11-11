"""E1: frozen CLIP, but the photo database also holds synthetic NOISY copies of the other photos.

No training. Each of the 210 clean photos gets noisy copies (5 noise types x levels in
noisy_copies.levels x noisy_copies.per_type, seed family 2026, never the test images). A query sees
every clean photo and copy EXCEPT those of its own photo (leave-one-photo-out), and the k nearest vote.

Why: at L3, 81 of 210 images have no correct disease among their 5 neighbours; noisy references
might match noisy queries better. Risk: L3 embeddings cluster by noise TYPE, not disease
(k-means ARI 1.00 vs -0.02), so copies of other diseases with the same noise may win.

    python scripts/noisy_database.py
    python scripts/noisy_database.py --set noisy_copies.levels=[3] --tag L3copies
"""
import _boot  # noqa: F401

import numpy as np

from safecrop.clip import ImageEncoder, load_clip, pick_device
from safecrop.config import cli, new_run_dir
from safecrop.data import load_manifest, missing_images
from safecrop.evaluate import database_vote, predictions_frame, reference_hits, with_truth, write_report
from safecrop.features import noisy_copy_embeddings, test_embeddings

args, cfg = cli(__doc__)
m = load_manifest(cfg)
assert not missing_images(cfg, m), "test images missing: run scripts/check_setup.py"
dev = pick_device(cfg["device"])
enc = ImageEncoder(load_clip(cfg["model"])).to(dev).eval()
V = test_embeddings(cfg, m, enc, dev, use_saved=cfg["use_saved_features"])
tab, X = noisy_copy_embeddings(cfg, m, enc, dev)

L0 = (m.level == "L0").to_numpy()
R = np.concatenate([V[L0], X])
r_label = np.concatenate([m.disease[L0].to_numpy(), tab.disease.to_numpy()])
r_photo = np.concatenate([m.photo_id[L0].to_numpy(), tab.photo_id.to_numpy()])
k = cfg["database"]["k"]
db = database_vote(V, m.photo_id, R, r_label, r_photo, k)
run = new_run_dir(cfg, "noisy_database", args.tag)
nc = cfg["noisy_copies"]
name = f"CLIP database + noisy copies (levels {nc['levels']}, x{nc['per_type']})"
p = predictions_frame(m.image, name, db)
p.to_csv(run / "predictions_database.csv", index=False)
df = with_truth(p, m)
from_copy = (db["nearest"] >= L0.sum()).mean(1)          # neighbours that are noisy copies (they come after the clean photos)
notes = [f"database = {L0.sum()} clean photos + {len(X)} noisy copies; k = {k}; leave-one-photo-out",
         f"share of the {k} neighbours that are noisy copies: L0 {from_copy[m.level == 'L0'].mean():.0%}, "
         f"L3 {from_copy[m.level == 'L3'].mean():.0%}"]
text = write_report(run, "E1: frozen CLIP + noisy copies in the database", {name: df}, m, notes,
                    extra_md=reference_hits(df, db["nearest_labels"]))
print(text)
print(f"\nSaved in {run}")
