"""E3: fine-tune CLIP's image encoder on clean + noisy copies, 5-fold cross-validation by photo.

Writes, for all scored images:
  predictions_database.csv  the Step 2 database vote with fine-tuned embeddings (compare with 40.0% at L3)
  predictions_head.csv      the 7-way classifier trained with the encoder (8-way with black gram)
  neighbours.csv            the 5 voting photos per image, same format as the Step 2b notebook's
                            clip_database_neighbours.csv, so Gemini + references can use them
  train_log.csv, summary.md, metrics.json

    python scripts/finetune.py --set finetune.folds=[0] --tag quick      # one fold (168 images) to try settings
    python scripts/finetune.py --tag k4_e15                              # all 5 folds = all 840 images
    python scripts/finetune.py --set finetune.epochs=0 --tag sanity      # no training: must equal the frozen baseline
    python scripts/finetune.py --set finetune.also_score_recipe_b=true   # also score recipe B with the SAME models
                                                                         # (a second run folder, tag + "_rb")
    python scripts/finetune.py --final                                   # train on all photos, save weights for the app
"""
import _boot  # noqa: F401

import time

import numpy as np
import pandas as pd
import torch

from safecrop.clip import pick_device, save_checkpoint
from safecrop.config import cli, dump_json, env_report, new_run_dir
from safecrop.data import fold_photos, load_manifest, missing_images
from safecrop.evaluate import predictions_frame, reference_hits, with_truth, write_report
from safecrop.finetune import final_checkpoint, score_fold, train_model


def write_outputs(cfg, m, run, folds, dbs, heads, nbs, timing, extra_notes=()):
    """Predictions, neighbours, timing and the report of one test set."""
    ft = cfg["finetune"]
    tag = f"k{ft['unfreeze_last']} e{ft['epochs']} cons{ft['consistency_weight']}"
    n_db = f"Fine-tuned CLIP database ({tag})" + (" + noisy copies" if ft.get("db_noisy_copies") else "")
    n_hd = f"Fine-tuned CLIP head ({tag})"
    pdb, phd = pd.concat(dbs, ignore_index=True), pd.concat(heads, ignore_index=True)
    pdb["model"], phd["model"] = n_db, n_hd
    pdb.to_csv(run / "predictions_database.csv", index=False)
    phd.to_csv(run / "predictions_head.csv", index=False)
    nbdf = pd.DataFrame(nbs, columns=["image", "rank", "ref_image", "ref_disease", "similarity"])
    nbdf["clip_model"] = f"{cfg['model']} fine-tuned ({run.name})"
    nbdf.to_csv(run / "neighbours.csv", index=False)
    dump_json({"folds": folds, "seconds_per_fold": timing}, run / "timing.json")

    new = {n_db: with_truth(pdb, m), n_hd: with_truth(phd, m)}
    nl = nbdf.sort_values(["image", "rank"]).groupby("image").ref_disease.apply(list)
    nearest_labels = np.array([nl[i] for i in new[n_db].image], dtype=object)
    notes = [f"folds {folds} (5-fold cross-validation by photo; each image scored by a model that never saw its photo)",
             f"model {cfg['model']}; unfreeze last {ft['unfreeze_last']} blocks; {ft['epochs']} epochs; lr {ft['lr']}; "
             f"consistency weight {ft['consistency_weight']}; noisy views {ft['noisy_views']} at levels {ft['train_levels']}",
             f"seconds per fold: {timing}", *extra_notes]
    print(write_report(run, "E3: fine-tuned CLIP", new, m, notes, extra_md=reference_hits(new[n_db], nearest_labels)))
    print(f"\nSaved in {run}")


def main():
    args, cfg = cli(__doc__, lambda ap: ap.add_argument(
        "--final", action="store_true", help="train on all photos and save the weights (no scores)"))
    m = load_manifest(cfg)
    assert not missing_images(cfg, m), "test images missing: run scripts/check_setup.py"
    dev = pick_device(cfg["device"])
    torch.manual_seed(int(cfg["seed"]))
    print(env_report(), "| device", dev)
    ft = cfg["finetune"]

    if args.final:
        run = new_run_dir(cfg, "finetune_final", args.tag)
        log = []
        f = final_checkpoint(cfg, m, dev, run / "encoder_all_photos.pt", log)
        pd.DataFrame(log).to_csv(run / "train_log.csv", index=False)
        print(f"Saved {f}. Do NOT score this model on the test images: it trained on every photo.")
        return

    # also score recipe B with the same trained models (only when training on the original test set)
    also_b = bool(ft.get("also_score_recipe_b")) and cfg["test_set"] == "original"
    sets = {"main": m}
    if also_b:
        sets["recipe_b"] = load_manifest({**cfg, "test_set": "recipe_b"})
        assert not missing_images(cfg, sets["recipe_b"]), "recipe-B images missing: run scripts/make_recipe_b.py"
    folds = [int(x) for x in (ft["folds"] if isinstance(ft["folds"], list) else [ft["folds"]])]
    run = new_run_dir(cfg, "finetune", args.tag)
    log, timing = [], {}
    out = {k: ([], [], []) for k in sets}                  # database predictions, head predictions, neighbours
    for fold in folds:
        train_ids, test_ids = fold_photos(m, fold)
        print(f"Fold {fold}: training on {len(train_ids)} photos, holding out {len(test_ids)}")
        t0 = time.time()
        enc, head, n_trainable = train_model(cfg, m, train_ids, dev, int(cfg["seed"]) + fold, log, str(fold))
        for k, mm in sets.items():
            q, db, hd, nb = score_fold(cfg, mm, enc, head, test_ids, dev)
            out[k][0].append(predictions_frame(q.image, "", db, {"fold": fold}))
            out[k][1].append(predictions_frame(q.image, "", hd, {"fold": fold}))
            out[k][2].extend(nb)
        timing[fold] = round(time.time() - t0, 1)
        if ft["save_checkpoints"]:
            save_checkpoint(enc, run / f"encoder_fold{fold}.pt", {"model": cfg["model"], "fold": fold,
                                                                 "unfreeze_last": int(ft["unfreeze_last"])})
        print(f"Fold {fold} done in {timing[fold]} s ({n_trainable / 1e6:.1f} M trainable weights)")
        del enc, head
        if dev.type == "cuda":
            torch.cuda.empty_cache()
        pd.DataFrame(log).to_csv(run / "train_log.csv", index=False)       # saved as we go

    write_outputs(cfg, m, run, folds, *out["main"], timing)
    if also_b:
        cfg_b = {**cfg, "test_set": "recipe_b"}
        run_b = new_run_dir(cfg_b, "finetune", f"{args.tag}_rb" if args.tag else "rb")
        pd.DataFrame(log).to_csv(run_b / "train_log.csv", index=False)
        write_outputs(cfg_b, sets["recipe_b"], run_b, folds, *out["recipe_b"], timing,
                      [f"the SAME trained models as run {run.name} (trained once on the test recipe's noise, "
                       "scored on both test sets; seconds per fold include both)"])


if __name__ == "__main__":      # needed on Mac/Windows: data-loading workers re-import this file
    main()
