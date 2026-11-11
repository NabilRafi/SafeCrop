"""Fine-tuning CLIP's image encoder on clean + synthetic noisy copies, scored with 5-fold cross-validation by photo.

Per fold: train on the clean L0 images of 168 photos (+ noisy copies made on the fly), then score the 42
held-out photos at all four levels (168 test images). After 5 folds every one of the 840 images has a
prediction from a model that never saw its photo. Two predictors come out of each model:
  * "database": the Step 2 photo database (5 nearest clean photos vote, leave-one-photo-out) with the
    fine-tuned embeddings -- directly comparable with the frozen CLIP database (40.0% at L3);
  * "head": a 7-way cosine classifier trained with the encoder.

Loss = cross-entropy on clean and noisy views + consistency_weight * (1 - cos(noisy, clean.detach())).
The consistency term pulls each noisy copy towards its own clean photo, so an L3 photo should land
next to clean photos of the same disease instead of next to other photos with the same noise.
"""
from __future__ import annotations

import math
import time

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader

from .clip import ImageEncoder, autocast, embed_arrays, embed_paths, load_clip, save_checkpoint, set_trainable
from .data import PairDataset, collate_pairs, disease_list, image_path, photos_table, read_rgb
from .evaluate import database_vote
from .features import noisy_copies_table
from .noise import make_noisy


class CosineHead(torch.nn.Module):
    def __init__(self, init: torch.Tensor, scale: float):
        super().__init__()
        self.W = torch.nn.Parameter(F.normalize(init.float(), dim=-1).clone())
        self.scale = scale

    def forward(self, z):
        return self.scale * F.normalize(z, dim=-1) @ F.normalize(self.W, dim=-1).T


def _schedule(total: int, warmup: int):
    def f(step):
        if warmup and step < warmup:
            return (step + 1) / warmup
        rest = max(1, total - warmup)
        return 0.5 * (1 + math.cos(math.pi * min(1.0, (step - warmup) / rest)))
    return f


def train_model(cfg: dict, m: pd.DataFrame, train_ids: list[str], device, seed: int, log_rows: list, fold_name: str):
    ft = cfg["finetune"]
    clip = load_clip(cfg["model"])
    if ft.get("grad_checkpointing"):
        clip.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    enc = ImageEncoder(clip).to(device)
    n_trainable = set_trainable(enc, int(ft["unfreeze_last"]))
    ds = PairDataset(cfg, m, train_ids, seed=seed, noisy_views=int(ft["noisy_views"]),
                     geometric_aug=bool(ft["geometric_aug"]), levels=tuple(ft["train_levels"]))
    # head starts as "nearest class mean" of the frozen clean training embeddings
    Z = torch.from_numpy(embed_arrays(enc, ds.images, device, cfg["batch_size"]))
    y = torch.tensor(ds.labels)
    init = torch.stack([Z[y == c].mean(0) for c in range(len(disease_list(m)))])
    head = CosineHead(init, float(ft["head_scale"])).to(device)
    epochs = int(ft["epochs"])
    if epochs == 0:
        return enc, head, n_trainable
    groups = [{"params": [p for p in enc.parameters() if p.requires_grad], "lr": float(ft["lr"])},
              {"params": list(head.parameters()), "lr": float(ft["head_lr"])}]
    opt = torch.optim.AdamW([g for g in groups if g["params"]], weight_decay=float(ft["weight_decay"]))
    g = torch.Generator()
    g.manual_seed(seed)
    loader = DataLoader(ds, batch_size=int(ft["batch_photos"]), shuffle=True, generator=g, drop_last=False,
                        num_workers=int(ft["num_workers"]), collate_fn=collate_pairs,
                        persistent_workers=False)
    steps = epochs * len(loader)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, _schedule(steps, int(round(float(ft["warmup_epochs"]) * len(loader)))))
    scaler = torch.amp.GradScaler("cuda") if device.type == "cuda" else None
    lam = float(ft["consistency_weight"])
    for epoch in range(epochs):
        ds.set_epoch(epoch)
        enc.train(); head.train()
        t0, tot, tot_ce, tot_cons, n = time.time(), 0.0, 0.0, 0.0, 0
        for x, yb in loader:
            B, V1 = x.shape[:2]
            xb = torch.from_numpy(x.reshape(B * V1, *x.shape[2:])).to(device)
            yv = torch.from_numpy(yb).to(device).repeat_interleave(V1)
            with autocast(device):
                z = enc(xb)
            z = z.view(B, V1, -1)
            ce = F.cross_entropy(head(z.reshape(B * V1, -1)), yv)
            cons = (1 - (z[:, 1:] * z[:, :1].detach()).sum(-1)).mean() if V1 > 1 else torch.zeros((), device=device)
            loss = ce + lam * cons
            opt.zero_grad(set_to_none=True)
            if scaler:
                scaler.scale(loss).backward()
                scaler.step(opt)
                scaler.update()
            else:
                loss.backward()
                opt.step()
            sched.step()
            tot += loss.item() * B; tot_ce += ce.item() * B; tot_cons += float(cons) * B; n += B
        row = {"fold": fold_name, "epoch": epoch + 1, "loss": tot / n, "ce": tot_ce / n, "consistency": tot_cons / n,
               "lr": sched.get_last_lr()[0], "seconds": round(time.time() - t0, 1)}
        log_rows.append(row)
        print(f"  fold {fold_name} epoch {epoch + 1}/{epochs}: loss {row['loss']:.4f} (ce {row['ce']:.4f}, "
              f"consistency {row['consistency']:.4f}) {row['seconds']}s", flush=True)
    enc.eval(); head.eval()
    return enc, head, n_trainable


@torch.no_grad()
def score_fold(cfg: dict, m: pd.DataFrame, enc: ImageEncoder, head: CosineHead, test_ids: list[str], device):
    """Predictions for the held-out photos' 4 levels with the fine-tuned model."""
    P = photos_table(m)
    R = embed_paths(enc, [image_path(cfg, im) for im in P.image], device, cfg["batch_size"])
    r_label, r_photo, r_image = P.disease.to_numpy(), P.photo_id.to_numpy(), P.image.to_numpy()
    if cfg["finetune"].get("db_noisy_copies"):
        nc = cfg["noisy_copies"]
        tab = noisy_copies_table(m, int(nc["per_type"]), nc["levels"], int(nc["seed"]))
        clean = {r.photo_id: read_rgb(image_path(cfg, r.image)) for r in P.itertuples()}
        X = embed_arrays(enc, [make_noisy(clean[r.photo_id], r.noise, r.level, r.seed) for r in tab.itertuples()],
                         device, cfg["batch_size"])
        R = np.concatenate([R, X])
        r_label = np.concatenate([r_label, tab.disease.to_numpy()])
        r_photo = np.concatenate([r_photo, tab.photo_id.to_numpy()])
        r_image = np.concatenate([r_image, (tab.clean_image + "#copy:" + tab.noise + ":L" + tab.level.astype(str)).to_numpy()])
    q = m[m.photo_id.isin(test_ids)].reset_index(drop=True)
    Q = embed_paths(enc, [image_path(cfg, im) for im in q.image], device, cfg["batch_size"])
    db = database_vote(Q, q.photo_id, R, r_label, r_photo, int(cfg["database"]["k"]))
    logits = head(torch.from_numpy(Q).to(device)).float()
    prob = logits.softmax(-1).cpu().numpy()
    order = np.argsort(-prob, 1)
    names = np.array(disease_list(m), dtype=object)
    hd = {"pred": names[order[:, 0]], "confidence": prob[np.arange(len(q)), order[:, 0]],
          "top3": np.array(["; ".join(names[o[:3]]) for o in order], dtype=object)}
    nb = [(q.image[i], r + 1, r_image[j], r_label[j], round(float(db["similarity"][i, r]), 4))
          for i in range(len(q)) for r, j in enumerate(db["nearest"][i])]
    return q, db, hd, nb


def final_checkpoint(cfg: dict, m: pd.DataFrame, device, out_file, log_rows: list):
    """Train on ALL 210 photos (for the app). Its scores on the 840 images would be meaningless: it saw every photo."""
    enc, head, _ = train_model(cfg, m, photos_table(m).photo_id.tolist(), device, int(cfg["seed"]), log_rows, "all")
    save_checkpoint(enc, out_file, {"model": cfg["model"], "unfreeze_last": int(cfg["finetune"]["unfreeze_last"]),
                                    "trained_on": "all 210 test photos (do not score on the 840 images)",
                                    "head_W": head.W.detach().cpu().numpy().tolist(), "classes": disease_list(m)})
    return out_file
