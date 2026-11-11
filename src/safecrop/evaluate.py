"""Scoring: the CLIP photo database vote, zero-shot, accuracy tables, McNemar tests, run reports.

Every predictor is scored on the same 840 images with the same tables the weekly slides use:
accuracy by level (L0-L3, all), info-rich (A) vs info-scarce (B), noise type, and head-to-head
McNemar exact tests against the saved baselines in data/baselines/.
"""
from __future__ import annotations

import csv
import datetime as _dt
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binomtest

from .config import ROOT
from .data import BLACK_GRAM, LEVELS, test_set_of
from .noise import NICE

TEST_SET_NAMES = {"recipe_b": "recipe B"}     # added to method names scored on another test set

BASELINES = {   # name -> file in data/baselines (per-image predictions on the 840 images)
    "CLIP database, frozen (Step 2)": "clip_database_7.csv",
    "Gemini + references + descriptions (Step 2b)": "gemini_refs_desc_step2b.csv",
    "Gemini plain, 33 options (Step 2)": "gemini_plain_33.csv",
    "CLIP zero-shot, 33 options (Step 2)": "clip_zero_shot_33.csv",
}
MAIN_BASELINES = list(BASELINES)[:2]      # what every new method must be tested against


# ----------------------------------------------------------------------------- predictors
def database_vote(Q: np.ndarray, q_photo, R: np.ndarray, r_label, r_photo, k: int = 5):
    """The Step 2 photo database: the k most similar reference images vote, weighted by similarity.

    Leave-one-photo-out: a query never sees ANY reference that comes from its own photo
    (its clean version, or noisy copies of it). Returns a dict of arrays: pred, confidence, top3,
    nearest (indices into R), nearest_labels.
    """
    q_photo, r_photo, r_label = np.asarray(q_photo), np.asarray(r_photo), np.asarray(r_label)
    S = (Q.astype(np.float32) @ R.astype(np.float32).T)
    S[q_photo[:, None] == r_photo[None, :]] = -np.inf
    k = max(1, min(k, R.shape[0] - 1))
    nearest = np.argsort(-S, axis=1)[:, :k]
    pred, conf, top3 = [], [], []
    for i in range(len(Q)):
        votes = {}
        for j in nearest[i]:
            votes[r_label[j]] = votes.get(r_label[j], 0.0) + max(float(S[i, j]), 0.0) + 1e-6
        ranked = sorted(votes.items(), key=lambda kv: -kv[1])
        pred.append(ranked[0][0])
        conf.append(ranked[0][1] / sum(votes.values()))
        top3.append("; ".join(d for d, _ in ranked[:3]))
    return {"pred": np.array(pred, dtype=object), "confidence": np.array(conf), "top3": np.array(top3, dtype=object),
            "nearest": nearest, "nearest_labels": r_label[nearest], "similarity": np.take_along_axis(S, nearest, 1)}


def zero_shot(V: np.ndarray, T: np.ndarray, keys, scale: float = 100.0):
    logits = scale * V @ T.T
    p = np.exp(logits - logits.max(1, keepdims=True))
    p /= p.sum(1, keepdims=True)
    order = np.argsort(-p, axis=1)
    keys = np.asarray(keys, dtype=object)
    return {"pred": keys[order[:, 0]], "confidence": p[np.arange(len(V)), order[:, 0]],
            "top3": np.array(["; ".join(keys[order[i, :3]]) for i in range(len(V))], dtype=object)}


def predictions_frame(images, model: str, out: dict, extra: dict | None = None) -> pd.DataFrame:
    df = pd.DataFrame({"image": list(images), "model": model, "pred_label": out["pred"],
                       "confidence": np.round(out["confidence"], 4), "top3": out.get("top3", "")})
    for k, v in (extra or {}).items():
        df[k] = v
    return df


# ----------------------------------------------------------------------------- truth and tables
def with_truth(pred: pd.DataFrame, m: pd.DataFrame) -> pd.DataFrame:
    """Adds the manifest columns and `correct` (pred_label == disease). Keeps only manifest images."""
    cols = ["image", "photo_id", "disease", "group", "noise", "level", "fold"]
    df = pred.drop(columns=[c for c in cols[1:] if c in pred.columns]).merge(m[cols], on="image", how="inner")
    df["correct"] = df.pred_label.astype(str).eq(df.disease)
    return df


def load_baselines(m: pd.DataFrame, names=None) -> dict[str, pd.DataFrame]:
    out = {}
    for name in (names or BASELINES):
        df = pd.read_csv(ROOT / "data" / "baselines" / BASELINES[name], keep_default_na=False)
        out[name] = with_truth(df[["image", "pred_label"]], m)
    return out


def pct(x) -> float:
    return round(100.0 * float(np.mean(x)), 1) if len(x) else float("nan")


def level_row(df: pd.DataFrame) -> dict:
    row = {lv: pct(df[df.level == lv].correct) for lv in LEVELS}
    row["All"] = pct(df.correct)
    row["n"] = len(df)
    return row


def md_table(rows: list[dict], first: str) -> str:
    cols = list(rows[0].keys())
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] + ["---:"] * (len(cols) - 1)) + " |"]
    for r in rows:
        lines.append("| " + " | ".join(f"{r[c]:.1f}" if isinstance(r[c], float) else str(r[c]) for c in cols) + " |")
    return "\n".join(lines)


def tables(named: dict[str, pd.DataFrame]) -> str:
    """Markdown tables: accuracy by level, by group, by noise type (L3 and L1-L3)."""
    out = ["### Accuracy by noise level (% correct)", "",
           md_table([{"Predictor": n, **level_row(df)} for n, df in named.items()], "Predictor"), ""]
    rows = []
    for n, df in named.items():
        r = {"Predictor": n}
        for g in "AB":
            d = df[df.group == g]
            r[f"{g} all"] = pct(d.correct)
            r[f"{g} L3"] = pct(d[d.level == "L3"].correct)
        rows.append(r)
    out += ["### Info-rich (A) vs info-scarce (B) (% correct)", "", md_table(rows, "Predictor"), ""]
    for lv_name, lv in [("L3", ["L3"]), ("L1-L3", ["L1", "L2", "L3"])]:
        rows = []
        for n, df in named.items():
            d = df[df.level.isin(lv)]
            rows.append({"Predictor": n, **{NICE[t]: pct(d[d.noise == t].correct) for t in NICE}})
        out += [f"### By noise type, {lv_name} (% correct)", "", md_table(rows, "Predictor"), ""]
    return "\n".join(out)


def mcnemar(a: pd.DataFrame, b: pd.DataFrame, level: str | None = None) -> dict:
    """Head to head on the images both predictors answered: only-a-right, only-b-right, exact p."""
    j = a[["image", "level", "correct"]].merge(b[["image", "correct"]], on="image", suffixes=("_a", "_b"))
    if level:
        j = j[j.level == level]
    oa = int((j.correct_a & ~j.correct_b).sum())
    ob = int((~j.correct_a & j.correct_b).sum())
    p = binomtest(oa, oa + ob, 0.5).pvalue if oa + ob else 1.0
    return {"images": len(j), "only_new_right": oa, "only_baseline_right": ob, "p": float(p)}


def fmt_p(p: float) -> str:
    return "<0.001" if p < 0.001 else f"{p:.3f}"


def head_to_head(new: dict[str, pd.DataFrame], baselines: dict[str, pd.DataFrame]) -> str:
    rows = []
    for nn, a in new.items():
        for bn, b in baselines.items():
            for lv in [None, "L3"]:
                r = mcnemar(a, b, lv)
                rows.append({"New": nn, "Baseline": bn, "Levels": lv or "All", "Images": r["images"],
                             "Only new right": r["only_new_right"], "Only baseline right": r["only_baseline_right"],
                             "p": fmt_p(r["p"])})
    if not rows:                    # nothing to test against (e.g. recipe B, where the baselines do not apply)
        return ""
    return "### Head to head (McNemar exact test)\n\n" + md_table(rows, "New") + "\n"


def reference_hits(df_truth: pd.DataFrame, nearest_labels: np.ndarray) -> str:
    """How many of the k database neighbours show the true disease (drives Gemini + references)."""
    hits = (nearest_labels == df_truth.disease.to_numpy()[:, None]).sum(1)
    rows = []
    for lv in LEVELS + ["All"]:
        sel = np.ones(len(df_truth), bool) if lv == "All" else (df_truth.level == lv).to_numpy()
        rows.append({"Level": lv, "Images": int(sel.sum()), "No correct neighbour": int((hits[sel] == 0).sum()),
                     "At least 1 correct (%)": pct(hits[sel] > 0), "Mean correct of k": round(float(hits[sel].mean()), 2)})
    return "### Correct neighbours among the k database photos\n\n" + md_table(rows, "Level") + "\n"


# ----------------------------------------------------------------------------- run report
def write_report(run_dir: Path, title: str, new: dict[str, pd.DataFrame], m: pd.DataFrame,
                 notes: list[str] | None = None, extra_md: str = "", compare_names=None) -> str:
    """summary.md + metrics.json in the run folder, one line per method in results/runs.csv. Returns the markdown.

    With black gram in the manifest (8 diseases) the tables come three times: the 840 original images first
    (comparable with every earlier number and baseline), then black gram only, then all images; runs.csv gets
    one line for the 840 original images and one for black gram.
    """
    ts = test_set_of(m)
    has_bg = bool((m.disease == BLACK_GRAM).any())
    tags = ([TEST_SET_NAMES.get(ts, ts)] if ts != "original" else []) + (["8 diseases"] if has_bg else [])
    if tags:                        # label every method with its test set / number of diseases
        new = {f"{n} [{', '.join(tags)}]": df for n, df in new.items()}
    if ts != "original":            # another test set: leave out the Step 2 / 2b baselines
        notes = (notes or []) + [f"TEST SET: {TEST_SET_NAMES.get(ts, ts)} = the same photos, noise types and folds, with "
                                 "L1-L3 made by a different noise recipe (src/safecrop/noise_b.py). The Step 2 / 2b "
                                 "baselines were scored on the original images, so they are not shown or tested here."]
    if has_bg:
        notes = (notes or []) + ["8 DISEASES: black gram yellow mosaic is an 8th choice (30 photos, 120 images, its own "
                                 "folds). The 840 original images come first so they stay comparable (these methods "
                                 "could also answer black gram, an 8th option the earlier 7-disease runs did not have)."]
    common = set.intersection(*[set(df.image) for df in new.values()])
    base = {} if ts != "original" else {
        k: v[v.image.isin(common)] for k, v in load_baselines(m, compare_names or list(BASELINES)).items()}
    base = {k: v for k, v in base.items() if len(v)}           # never show a baseline with no shared images
    main = {k: v for k, v in base.items() if k in (compare_names or MAIN_BASELINES)}
    md = [f"# {title}", "", f"Run folder: `{run_dir.relative_to(ROOT) if run_dir.is_relative_to(ROOT) else run_dir}`", ""]
    if len(common) < len(m):
        notes = (notes or []) + [f"PARTIAL: scored on {len(common)} of {len(m)} images; baselines below use the same images."]
    md += [f"- {n}" for n in (notes or [])] + [""]
    old = {n: df[df.disease != BLACK_GRAM] for n, df in new.items()}      # the 840 original images
    bg = {n: df[df.disease == BLACK_GRAM] for n, df in new.items()}
    if has_bg:
        md += ["## The original images (7 diseases): comparable with every earlier number", "",
               tables({**old, **base}), head_to_head(old, main),
               "## Black gram yellow mosaic only (no earlier baselines)", "", tables(bg),
               "## All images (8 diseases)", "", tables(new), extra_md]
    else:
        md += [tables({**new, **base}), head_to_head(new, main), extra_md]
    text = "\n".join(md)
    (run_dir / "summary.md").write_text(text)
    metrics = {}
    for n in new:
        d = old[n]
        metrics[n] = {"levels": level_row(d), "A": pct(d[d.group == "A"].correct), "B": pct(d[d.group == "B"].correct),
                      "vs": {bn: {lv or "All": mcnemar(d, b, lv) for lv in [None, "L3"]} for bn, b in main.items()}}
        if has_bg:
            metrics[n].update(black_gram=level_row(bg[n]), all_images=level_row(new[n]))
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=1))
    log = run_dir.parent.parent / "runs.csv"           # results/runs.csv: one line per method per run
    first = not log.exists()

    def blank(x):
        return "" if isinstance(x, float) and np.isnan(x) else x

    with open(log, "a", newline="") as f:
        w = csv.writer(f)
        if first:
            w.writerow(["time", "run_dir", "method", "n", "L0", "L1", "L2", "L3", "All", "A", "B",
                        "L3_vs_frozen_db_new", "L3_vs_frozen_db_old", "L3_vs_frozen_db_p"])
        now = _dt.datetime.now().isoformat(timespec="seconds")
        for n in new:
            parts = [(n + (" (original 7 diseases)" if has_bg else ""), old[n], True)]
            if has_bg:
                parts.append((n + " (black gram only)", bg[n], False))
            for name, d, with_vs in parts:
                lr = level_row(d)
                v = metrics[n]["vs"].get(MAIN_BASELINES[0], {}).get("L3", {}) if with_vs else {}
                w.writerow([now, str(run_dir.name), name, lr["n"], *[blank(lr[k]) for k in ["L0", "L1", "L2", "L3", "All"]],
                            blank(pct(d[d.group == "A"].correct)), blank(pct(d[d.group == "B"].correct)),
                            v.get("only_new_right", ""), v.get("only_baseline_right", ""),
                            round(v["p"], 4) if v else ""])
    return text
