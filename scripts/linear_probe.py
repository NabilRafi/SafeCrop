"""E2: a classic classifier on FROZEN CLIP features, 5-fold cross-validation by photo.

linear_probe.classifier = logistic (linear probe) or svm (RBF SVM: the "traditional ML on CLIP
features" baseline promised in the mid-project report). Training data per fold: the clean images of
the 168 training photos (+ their synthetic noisy copies if linear_probe.use_copies). Test: the 42
held-out photos at all 4 levels, so every image is predicted by a model that never saw its photo.

    python scripts/linear_probe.py
    python scripts/linear_probe.py --set linear_probe.classifier=svm --tag svm
    python scripts/linear_probe.py --set linear_probe.use_copies=false --tag clean_only
"""
import _boot  # noqa: F401

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.svm import SVC

from safecrop.clip import ImageEncoder, load_clip, pick_device
from safecrop.config import cli, new_run_dir
from safecrop.data import fold_photos, load_manifest, missing_images
from safecrop.evaluate import predictions_frame, with_truth, write_report
from safecrop.features import CACHED_MODEL, noisy_copy_embeddings, test_embeddings

args, cfg = cli(__doc__)
m = load_manifest(cfg)
assert not missing_images(cfg, m), "test images missing: run scripts/check_setup.py"
dev = pick_device(cfg["device"])
use_copies = bool(cfg["linear_probe"]["use_copies"])
kind = cfg["linear_probe"]["classifier"]
assert kind in ("logistic", "svm"), "linear_probe.classifier must be logistic or svm"
need_model = use_copies or not (cfg["use_saved_features"] and cfg["model"] == CACHED_MODEL
                                and cfg["test_set"] == "original")
enc = ImageEncoder(load_clip(cfg["model"])).to(dev).eval() if need_model else None   # saved features: no model needed
V = test_embeddings(cfg, m, enc, dev, use_saved=cfg["use_saved_features"])
if use_copies:
    tab, X = noisy_copy_embeddings(cfg, m, enc, dev)

C_GRID = [0.1, 1.0, 10.0, 100.0]


def make(C, final=False):
    if kind == "svm":
        return SVC(kernel="rbf", C=C, probability=final, random_state=int(cfg["seed"]))
    return LogisticRegression(C=C, max_iter=5000)


def choose_C(Xtr, ytr, groups):
    """Pick C inside the training photos only (4-fold by photo), never on the held-out fold."""
    scores = {}
    for C in C_GRID:
        acc = []
        for a, b in GroupKFold(n_splits=4).split(Xtr, ytr, groups):
            acc.append((make(C).fit(Xtr[a], ytr[a]).predict(Xtr[b]) == ytr[b]).mean())
        scores[C] = float(np.mean(acc))
    return max(scores, key=scores.get), scores


parts, chosen = [], {}
for fold in range(5):
    train_ids, test_ids = fold_photos(m, fold)
    tr = (m.level == "L0") & m.photo_id.isin(train_ids)
    Xtr, ytr, gtr = V[tr.to_numpy()], m.disease[tr].to_numpy(), m.photo_id[tr].to_numpy()
    if use_copies:
        sel = tab.photo_id.isin(train_ids).to_numpy()
        Xtr, ytr = np.concatenate([Xtr, X[sel]]), np.concatenate([ytr, tab.disease.to_numpy()[sel]])
        gtr = np.concatenate([gtr, tab.photo_id.to_numpy()[sel]])
    C = cfg["linear_probe"]["C"]
    C, grid = choose_C(Xtr, ytr, gtr) if str(C) == "auto" else (float(C), {})
    chosen[fold] = C
    clf = make(C, final=True).fit(Xtr, ytr)
    te = m.photo_id.isin(test_ids).to_numpy()
    prob = clf.predict_proba(V[te])
    order = np.argsort(-prob, 1)
    cls = clf.classes_
    out = {"pred": cls[order[:, 0]], "confidence": prob[np.arange(len(prob)), order[:, 0]],
           "top3": np.array(["; ".join(cls[o[:3]]) for o in order], dtype=object)}
    parts.append(predictions_frame(m.image[te], "", out, {"fold": fold}))
    print(f"  fold {fold}: C = {C}, trained on {len(ytr)} vectors, scored {te.sum()} images"
          + (f" (inner accuracy by C: {', '.join(f'{c:g}: {v:.3f}' for c, v in grid.items())})" if grid else ""))

name = ("SVM" if kind == "svm" else "Linear probe") + " on frozen CLIP" + (" (clean + noisy copies)" if use_copies else " (clean only)")
p = pd.concat(parts, ignore_index=True)
p["model"] = name
run = new_run_dir(cfg, "linear_probe", args.tag)
p.to_csv(run / "predictions_probe.csv", index=False)
notes = ["5-fold cross-validation by photo (folds fixed in data/manifest.csv)",
         f"{'RBF SVM' if kind == 'svm' else 'logistic regression'}; C per fold {chosen}"
         + (" (chosen by 4-fold CV inside the training photos)" if str(cfg["linear_probe"]["C"]) == "auto" else "")
         + f"; classes = the {m.disease.nunique()} test diseases"]
print(write_report(run, f"E2: {name}", {name: with_truth(p, m)}, m, notes))
print(f"\nSaved in {run}")
