# Fine-tuning plan (Week 9, 9-15 Nov 2026)

Goal: a CLIP model that recognises **severely noisy (L3)** photos better than frozen CLIP, measured
exactly like every earlier SafeCrop number, so the final report can put it in the four-way comparison
(SVM on CLIP features, fine-tuned CLIP, CLIP photo database, Gemini).

> **Update 11 Nov: a much higher bar.** The Colab noisy reference album (each reference photo plus 15
> noisy copies, no training) reached 93.8-95.2% at L3 on our 7 diseases (85.7-88.1% with healthy /
> look-alike leaves added), against 40.0% for the frozen database. E3/E4 must be compared with that, not
> only with 40.0%. E1 below is the same design as the album's Idea 1, so it gives this kit its own
> noisy-album baseline (per-image predictions for McNemar). The album's copies use the test set's own
> noise recipe (a best case), so the open questions are a different noise recipe and real photos.
> Details: `docs/PROJECT_HISTORY.md`, Week 9.

## Why fine-tuning should help (and where it can fail)

| Finding so far | What it suggests |
| --- | --- |
| At L3 the frozen database is 40.0% right; 81 of 210 L3 images have **no** correct disease among their 5 neighbours | The embedding of an L3 photo lands near the wrong clean photos. Training on noisy copies can move it back. |
| Frozen L3 embeddings cluster by **noise type** (k-means ARI 1.00), not disease (ARI -0.02) | The model "sees the noise" first. A consistency loss (noisy copy close to its own clean photo) attacks exactly this. |
| Gemini + references uses a label shown in its references 98.6% of the time; with 0 correct references it was right 1 time in 123 | Better neighbours from a fine-tuned CLIP should also lift Gemini + references (E5). |
| ~20 image edits never beat the photo as taken (except resample for JPEG) | Fix the model, not the photo. |
| Clean-only SVM / logistic probe on frozen features: 76.0% / 68.8% (L3 37.1% / 26.2%) | Without noisy training data a classifier does not beat the database. |
| Each disease comes from one photo source (style matching); 30 photos per disease | Risk of over-fitting to style and to few photos: keep the cross-validation strict, prefer few trainable layers, look at A vs B and per-disease results. |

## Evaluation protocol (fixed before any training)

- **Test set:** the 840 images. **Folds:** `data/manifest.csv` column `fold` (5 folds by photo,
  42 photos each, balanced by disease; noise types 7-10 per fold). For fold f, train only on photos with
  `fold != f`, score the 168 images (4 levels) of photos with `fold == f`. After 5 folds all 840 images
  are scored by a model that never saw their photo.
- **Training images:** the clean L0 images of training photos + noisy copies made on the fly
  (random noise type, random level L1-L3, fresh seeds, random flip/quarter turn). The fixed L1-L3 test
  files are never read for training (they are just one sample of the same recipe).
- **Two predictors per model:**
  1. *database*: the Step 2 vote (k = 5, cosine-weighted, leave-one-photo-out) with fine-tuned
     embeddings of all 210 clean photos as references. Directly comparable with 40.0% at L3.
  2. *head*: the 7-way cosine classifier trained with the encoder.
- **Tables (automatic in summary.md):** accuracy by level and overall; A vs B (all, L3); by noise type
  (L3 and L1-L3); McNemar vs frozen database and vs Gemini + references (all levels and L3);
  correct-neighbour table (images with 0 correct neighbours at L3; frozen: 81 of 210).
- **Settings search:** try settings on fold 0 only (`--set finetune.folds=[0]`), compare with the frozen
  database on the same 168 images (the summary does this), then fix the settings and run all 5 folds.
  Keep `results/runs.csv`: the report says how many settings were tried.
- **Sanity checks:** `--set finetune.epochs=0` must give the frozen database's predictions (no training);
  `scripts/smoke_test.py` after code changes.

## Experiments

### E0. Frozen baseline from the images
`python scripts/reproduce_baseline.py` recomputes ViT-L/14 embeddings and must give
100 / 93.3 / 71.9 / 40.0 (all 76.3). A handful of predictions may flip between GPU fp16 and CPU/Mac fp32.
Its `neighbours.csv` is in the Step 2b format.

### E1. Noisy copies in the database (no training)
`python scripts/noisy_database.py`. Database = 210 clean photos + 3,150 noisy copies (5 types x 3 levels),
leave-one-photo-out. Same design as the Colab noisy album's Idea 1 (95.2% at L3), so expect a similar
number; a big gap means the kit and the notebook differ somewhere. Variants: `--set noisy_copies.levels=[3]`,
`--set noisy_copies.per_type=2`.
Watch the share of neighbours that are copies and whether L0-L1 drop (copies of other diseases with the
same noise may win: the noise-type clustering risk).

### E2. Classic classifiers on frozen features (also the SVM baseline for the report)
`python scripts/linear_probe.py` (logistic) and `--set linear_probe.classifier=svm`. Train on clean +
noisy copies of training photos, 5 folds; C chosen inside the training photos. Clean-only reference:
`--set linear_probe.use_copies=false` (SVM 76.0%, L3 37.1%).

### E3. Fine-tuning (main experiment)
`python scripts/finetune.py`. Default: ViT-L/14, last 4 of 24 blocks + final norm + projection trainable
(~50 M weights), 15 epochs, 16 photos per step (each 1 clean + 1 noisy view), AdamW lr 1e-5 (head 1e-3),
cosine schedule with 1 warm-up epoch, loss = cross-entropy (clean + noisy) + 1.0 x (1 - cos(noisy, clean)).

Suggested order on fold 0 (each ~2-4 min on a Colab T4):
1. defaults
2. `finetune.consistency_weight` 0 vs 1 vs 3 (does the consistency term matter?)
3. `finetune.unfreeze_last` 2 / 4 / 8
4. `finetune.epochs` 8 / 15 / 30, `finetune.noisy_views` 1 vs 2, `finetune.train_levels` [3] vs [1,2,3]
Then run all 5 folds with the chosen settings, plus the defaults (so the report has both).

### E4. Fine-tuned encoder + fine-tuned noisy copies in the database
`--set finetune.db_noisy_copies=true` (adds ~3,150 embeddings per fold).

### E5. Gemini + references with fine-tuned neighbours
Take `neighbours.csv` from the best E3/E4 run (same columns as the Step 2b notebook's
`clip_database_neighbours.csv`), put it where the Step 2b notebook reads that file, and run Gemini with
`GEMINI_LEVELS = ["L3"]` first (210 requests, within one day's free quota). Compare with Step 2b (47.1%).

### E6. Next ideas (only after E3)
- **Healthy/look-alike negatives:** add the 240 PlantVillage extras (`data/extra_references/`, see
  `data/extra_references.csv`; never potato late blight or grape leaf blight from PlantVillage) as extra
  classes or as negatives, then test the "filled database" (frozen: 15% at L3).
- **More photos per disease from the source datasets** (AppleLeaf9, DiaMOS, Mendeley stem borer, Harvard
  jute, PlantVillage for potato/grape) for training, excluding the 210 test photos by file hash. Then the
  840 images become a pure test set (no cross-validation needed).
- Prompt-tuned text side (CoOp-style) so zero-shot uses the fine-tuned image space.
- Fine-tuned CLIP inside the retake loop (stop rule qc >= 0.8) and in the app.

### E7. Robustness: recipe B (built 11 Nov)
On the original noise, every method that learned it reaches 95-98% at L3 (E1, E2, E4), so they can no
longer be told apart there. Recipe B keeps the photos, noise types, levels and folds but makes the noise a
different way (`src/safecrop/noise_b.py`); each level is matched to the test images' damage by levelled
colour MS-SSIM (multi-scale; brightness and contrast matched per colour channel first; no model, no labels).
Nothing is retrained: every method still learns only from the test recipe, then is scored on recipe B with
`--set test_set=recipe_b` (fine-tuning: `--set finetune.also_score_recipe_b=true` scores both test sets with the
same trained models).
`scripts/robustness.py` reports accuracy on the test recipe vs recipe B with a paired McNemar test (same
photo, same level) and the methods against each other on recipe B. The frozen database (E0) on recipe B
shows how hard recipe B is for a model that never saw any noise.

## Compute estimates (ViT-L/14)

| Step | Colab T4 | Apple M-series (mps) | CPU only |
| --- | --- | --- | --- |
| Embed 840 test images | ~30 s | ~2 min | ~10 min |
| Noisy copies (3,150 images) | ~2 min | ~6 min | ~40 min |
| Fine-tune one fold (15 epochs) | ~3-5 min | ~15-30 min | not practical |
| All 5 folds | ~15-25 min | ~1.5-2.5 h | not practical |

Rough figures; the first run also downloads the weights (~1.7 GB, cached in `~/.cache/huggingface`).
Out of GPU memory: `--set finetune.batch_photos=8` or `--set finetune.grad_checkpointing=true`.

## What goes on the Week 9 slides

1. Table: E0-E4 + noisy album + Gemini + references by level (L0-L3, all), the four-way comparison.
2. Table: McNemar vs frozen database and vs Gemini + references (all, L3).
3. Table: A vs B and by noise type at L3.
4. Table: images with no correct neighbour at L3 (frozen 81 of 210, noisy album 2 -> ?).
5. One line each: settings tried (from runs.csv), time per fold, GPU used.
