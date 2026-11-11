# SafeCrop: CLIP fine-tuning (project memory for Claude Code)

Read this first. Details live in `docs/` (read them when a task needs them):
`docs/PROJECT_HISTORY.md` (every result so far), `docs/FINETUNING_PLAN.md` (experiments E0-E6),
`docs/DATA.md` (sources, licences, caveats), `docs/reference/` (the original project notes).

## The project in five lines

SafeCrop is the CSE299 Junior Design project (North South University, Fall 2026, Section 13, Group 7;
supervisor Md. Salman Shamil; course Track 3, "ML model and dataset development").
It asks how **photo noise** and **how well-studied a disease is** (info-rich vs info-scarce) change
AI crop-disease diagnosis from phone photos, and adds an agentic loop that asks for a clearer photo
only when the model is unsure. Track 3 compares a traditional method (SVM on CLIP features),
a **fine-tuned model (this repo)**, the CLIP photo database and a zero-shot LLM API (Gemini) on the same 840 images.

**This repo's job (Week 9, due Sunday 15 Nov 2026):** fine-tune CLIP so severely noisy (L3) photos are
recognised better, scored so that every number is directly comparable with the earlier ones.

## Who you are working with

- **Nabil** (Mohammad Nabil Ferdous) writes and runs the code with you. Explain plainly and briefly:
  short sentences, no unexplained jargon, one idea at a time. He has said explanations get confusing; check
  that yours is easy to follow. Say what you are about to run and roughly how long it takes.
- **The supervisor wants numbers, not descriptions**: tables with n, accuracy by level, A vs B,
  and McNemar p-values against the baselines. Every experiment ends in `summary.md` tables that can
  go straight onto a slide. Weekly updates are a Google Slides deck presented on Sundays.

## Hard rules (do not break these)

1. **No test-photo leakage.** Score with the fixed 5 folds in `data/manifest.csv` (`fold`, by photo:
   42 photos per fold) or with leave-one-photo-out. A model or database must never contain any
   version (clean, noisy, rotated, augmented) of the photo it is scoring. Training noise uses fresh
   seeds; never use seed family 299 (the test set's) for training data.
2. **PlantVillage duplicates.** All 25 potato late blight and 30 grape leaf blight test photos ARE
   PlantVillage images. Never add PlantVillage potato late blight or grape leaf blight images to training
   or reference data. (PlantVillage apple scab is a genuinely different source: allowed.)
3. **Same yardstick.** Score on the same 840 images (or say clearly which subset), with the tables in
   `src/safecrop/evaluate.py`, and test against the frozen CLIP database (Step 2) and Gemini + references
   (Step 2b) with McNemar. Every run is logged in `results/runs.csv`: report how many settings were
   tried, never only the best one. Choose settings on fold 0 (`--set finetune.folds=[0]`), then fix them
   and run all 5 folds once.
4. **Free only.** Nabil will not use a credit card or any card, not even for free trials that ask for one.
   No paid APIs or cloud credits. GPUs: his own machine or free Google Colab. Gemini only via the free
   AI Studio key (`gemini-3.5-flash-lite`: 15 requests/min, 500/day; resets 2 pm Dhaka time).
5. **Never print, log, commit or hard-code an API key.** `GEMINI_API_KEY` lives in `.env` (git-ignored)
   or Colab secrets. This repo does not need it for CLIP work.
6. **Frozen record.** Do not edit `data/manifest.csv`, `data/labels.csv`, `data/baselines/`,
   `data/features/`, `data/images/`. New outputs go in `results/` (one folder per run, never overwritten).
7. **Models in scope:** CLIP (`openai/clip-vit-large-patch14` for all reported numbers) and Gemini 3.5
   Flash-Lite. Gemma (25.6% vs Gemini's 38.9% on 180 images) and Gemini 3.8 Flash were dropped. ViT-B/16
   is fine for quick tries (`configs/vitb16_fast.yaml`), but compare it with its own frozen baseline.
8. After changing code, run `python scripts/smoke_test.py` (tiny random model, ~2 min on CPU) before
   spending GPU time.

## The data (details: docs/DATA.md)

- **840 test images = 210 photos x 4 levels**, 224 x 224 PNG, in `data/images/L{0..3}/<disease>/`.
  Names: `L0/apple_scab/apple_scab_001_clean_L0.png`, `L3/jute_mosaic/jute_mosaic_007_motion_blur_L3.png`.
- `data/manifest.csv`: one row per image: `image, photo_id, disease, disease_name, group (A/B), origin
  (Local/Foreign), noise, level (L0-L3), severity, fold (0-4), source_file`.
- **7 diseases.** Group A, info-rich: apple scab (30 photos), potato late blight (25), rice stem borer (30).
  Group B, info-scarce: grape leaf blight (30), pear leaf spot (35), jute mosaic (30), jute dieback (30).
  Local (Bangladesh): rice stem borer, jute mosaic, jute dieback.
- **Black gram yellow mosaic (8th disease), an extension added to this repo on 11 Nov.** 30 clean photos
  (512 x 512 originals; group A, Local, index 0.65; 6 photos per noise type), noised in the Colab notebook
  `SafeCrop_make_noisy_images_with_black_gram.ipynb` (same recipe and seeds). In the repo:
  `data/images_black_gram/L{0..3}/black_gram_yellow_mosaic/` (120 PNGs, kept apart so `data/images/` stays the
  frozen 840; recipe check: 88/90 noisy images identical, 90/90 within 1 grey level) and
  `data/manifest_black_gram.csv` (120 rows; its own folds: 6 photos per fold, every noise type in every fold,
  seeded shuffle 299), both from `scripts/add_black_gram.py`. `data/manifest.csv`, the 210 photos' folds, saved
  features and baselines are unchanged and cover only the 840 images / 7 diseases. Score with
  `--set black_gram=true` (8 diseases, 960 images): reports show the 840 original images first (comparable,
  with the Step 2 / 2b tests), then black gram only, then all 960; `runs.csv` gets one line for each part.
  Always report the 7 old diseases and black gram separately.
- **One noise type per photo** (42 photos each), at L1 mild, L2 medium, L3 severe:

  | Noise | Imitates | L1 / L2 / L3 |
  | --- | --- | --- |
  | gaussian_noise (sensor noise) | grainy cheap camera | strength 0.08 / 0.18 / 0.38 |
  | motion_blur (hand-shake blur) | phone moved | blur length 10 / 15 / 20 px |
  | defocus_blur (out of focus) | focused on the background | radius 3 / 6 / 10 px |
  | low_light | evening or shade | 30% / 12% / 5% of the light |
  | jpeg_compression | sent over Messenger/WhatsApp | quality 25 / 15 / 7 |

  `src/safecrop/noise.py` is the exact recipe: `make_noisy(L0, noise, level, seed_for(photo_id, noise, level))`
  rebuilds the test images (612/630 bit-identical, the rest within 1 grey level).
- **Recipe B (robustness test, E7, built 11 Nov):** the same 210 clean photos, noise types, levels and folds,
  but L1-L3 made a different way (`src/safecrop/noise_b.py`: brightness-dependent clumped grain, curved shake,
  Gaussian defocus + colour fringes, auto-exposed low light, shrink + WebP). Each level's strength matches
  the test images' damage by levelled colour MS-SSIM (multi-scale; brightness/contrast matched per channel
  first; no model or labels used; every level within 0.001). Seeds 4242 (calibration 5005).
  `data/manifest_recipe_b.csv` (960 rows incl. black gram; image names start with `recipe_b/`, so they never
  mix with the 840; L0 rows are the original clean files) + `data/images_recipe_b/` (720 PNGs, rebuilt by
  `scripts/make_recipe_b.py`; not in the Colab code zip, so run that script first on Colab). Score any script on it with `--set test_set=recipe_b`: reports then skip the
  Step 2/2b baselines (they were scored on the original images) and tag every method "[recipe B]".
- `data/labels.csv`: the 33 options used by CLIP zero-shot and Gemini (7 test diseases + same-crop
  look-alikes + "healthy" for each crop), with Gemini's one-line descriptions.
- `data/features/clip_vitl14_frozen.npz`: the Step 2 frozen ViT-L/14 features (V 840x768, T 33x768,
  X = 240 PlantVillage extras). They reproduce the Step 2 predictions exactly (840/840).
- `data/baselines/`: per-image predictions of every earlier method (see `data/README.md`).
- Known caveats: each disease comes from one photo source, so CLIP can partly match photo **style**
  (apple scab with other-source references only: 100% -> 7% on clean photos); potato and grape are
  PlantVillage lab photos; noise is synthetic; ±7 points chance variation per level (210 images).

## Baselines to beat (all 840 images, % correct)

| Predictor | L0 | L1 | L2 | L3 | All | A all | B all |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Gemini 3.5 Flash-Lite + 5 reference photos + descriptions (Step 2b) | 100 | 92.9 | 75.2 | **47.1** | **78.8** | 80.6 | 77.6 |
| CLIP photo database, frozen ViT-L/14 (Step 2) | 100 | 93.3 | 71.9 | **40.0** | 76.3 | 81.2 | 73.0 |
| Gemini 3.5 Flash-Lite, plain, 33 options | 66.7 | 48.6 | 26.2 | 12.9 | 38.6 | 54.7 | 27.6 |
| CLIP zero-shot, 33 options | 25.7 | 15.2 | 8.6 | 3.8 | 13.3 | | |

CLIP database = the 5 most similar clean (L0) photos of OTHER photos vote, weighted by cosine similarity,
among the 7 diseases (leave-one-photo-out). Gemini + references gets exactly those 5 photos. Step 2b vs
database: all levels 33 vs 12 (p = 0.003), L3 18 vs 3 (p = 0.002). Same 7 choices at L3: plain Gemini
41.0% vs database 40.0% (p = 0.90).

**New bar (8-11 Nov): the noisy reference album** (Colab `SafeCrop_noisy_album_idea2.ipynb`, not in this
repo; details in `docs/PROJECT_HISTORY.md`, Week 9). Supervisor's advice: compare noisy photos with noisy
photos. Every album photo gets 15 noisy copies (5 types x L1-L3, seed family 2026), leave-one-photo-out,
same ViT-L/14 and k = 5 vote. Idea 1 = one mixed album (clean + all copies); Idea 2 = one album per noise
type + level, picked by the photo check. L3, % correct of 210 images:

| Album | Frozen, clean only | Idea 2 | Idea 1 | L3 images with no correct neighbour |
| --- | ---: | ---: | ---: | ---: |
| Our 7 diseases | 40.0 | 93.8 | **95.2** | 81 -> 2 |
| Filled: + 210 PlantVillage healthy / look-alike leaves | 15.2 | 85.7 | 88.1 | 151 -> 6 |

The copies do the work, not the matching (Idea 1 is as good or better, no photo check needed). Filled album:
"called healthy" at L3 73% -> 5%, L0 unchanged (99.5%). The A vs B gap disappears. **This is a best case:**
the copies use the test set's own noise recipe, and the first real field photo (potato late blight) was
called apple scab by all three albums (the album has only PlantVillage lab photos of potato).

## What we already know that matters for fine-tuning

- **Noisy reference photos already fix most of L3, with no training** (noisy album above: 40.0% -> 95.2%).
  Fine-tuning (E3/E4) must be compared with that, not only with 40.0%. Because the album uses the test
  set's own noise recipe, the open questions are a different noise recipe and real photos.
- **L3 is the problem.** Every method loses most accuracy at L3; L0-L1 are near 100% for CLIP.
- **Missing references cap everything.** At L3, 81 of 210 images have no correct disease among their
  5 database neighbours (123 images over all levels, and Gemini + references got just 1 of those 123
  right; the noisy album cuts the 81 to 2). Better neighbours should lift BOTH the database and
  Gemini + references (Gemini picks a label shown in its references 98.6% of the time). So the database
  vote with fine-tuned embeddings, and its `neighbours.csv`, are the main outputs, not only a classifier head.
- **L3 embeddings cluster by noise type, not disease** (k-means on frozen L3 features: ARI 1.00 for noise
  type vs -0.02 for disease). This is why `finetune.consistency_weight` pulls each noisy view towards
  its own clean photo.
- **Healthy-leaf pull.** With 240 PlantVillage look-alike/healthy photos added to the database, CLIP at L3
  fell 40% -> 15%: 73% of L3 photos were called a healthy leaf (closest healthy apple 0.72 vs closest
  own-disease photo 0.68). Plain Gemini also answers some crop's "healthy" for 48% of L3 photos.
  The noisy album fixes most of this: "called healthy" at L3 73% -> 5%.
- **Fixing the photo does not work; fixing the model side might.** Of ~20 image edits at L3 none helped
  except resample (shrink + enlarge) on JPEG photos (57% -> 79%); zoom broke 44 images and fixed none.
  Retry pipelines never beat one try. Learned fix choice: 40.0 -> 47.1% (mostly from compression).
- **Clean-only classifiers don't help** (run on 8 Nov while building this kit: saved features, 5 folds, C
  chosen inside the training photos; rerun with `scripts/linear_probe.py --set linear_probe.use_copies=false`):
  logistic probe 68.8% (L3 26.2%); RBF SVM 76.0% (L3 37.1%; A 80.6, B 72.8) vs database 76.3% (40.0%):
  SVM vs database 23 vs 26 images (p = 0.78), at L3 9 vs 15 (p = 0.31). Noisy training data is the lever.
- Photos beat words: descriptions alone add ~5 points at L3; reference photos add ~29.
- 1 clean photo per disease still gives the database 35% at L3 (all ~29 per disease: 40%).
- Retake loop (asking for a clearer photo): from L3 CLIP ends 88% right after ~2.6 photos; carrying the
  previous photo's features always hurt. Fine-tuned CLIP should later be dropped into that loop.

## The plan (details and success criteria: docs/FINETUNING_PLAN.md)

| ID | Experiment | Script | Needs |
| --- | --- | --- | --- |
| E0 | Frozen baseline recomputed from images (must give 100/93.3/71.9/40.0) | `scripts/reproduce_baseline.py` | any machine |
| E1 | Frozen CLIP + noisy copies of the other photos in the database (same design as the noisy album's Idea 1) | `scripts/noisy_database.py` | any (GPU faster) |
| E2 | Logistic probe / SVM on frozen features + noisy copies, 5 folds | `scripts/linear_probe.py` | any |
| E3 | Fine-tune last 4 blocks + projection: CE + noise consistency, 5 folds | `scripts/finetune.py` | GPU |
| E4 | E3 + fine-tuned noisy copies in the database | `scripts/finetune.py --set finetune.db_noisy_copies=true` | GPU |
| E5 | Gemini + references with the fine-tuned neighbours (L3 first, quota!) | Step 2b notebook + `neighbours.csv` | free Gemini key |
| E6 | Healthy/look-alike negatives; train on extra photos from the source datasets | to build | GPU, data |
| E7 | Robustness: every method scored on recipe B (same photos, noise made a different way) | `make_recipe_b.py`, `--set test_set=recipe_b`, `robustness.py` | GPU for E3/E4 |

**Done (11 Nov):** E0 = Step 2 exactly (0 of 840 answers changed). E1 (Colab) = 100 / 100 / 99.0 / **95.2**,
all 98.6: this kit's noisy-album baseline; per-image predictions in
`results/noisy_database/20261111-120939_clip-vit-large-patch14_e1/predictions_database.csv`. Only 10 L3
images are still wrong, so E3/E4 can hardly beat E1 significantly on these 840 images. E2 SVM (clean +
noisy copies, 5 folds) = 100 / 99.5 / 99.0 / **97.6**, all 99.0 (vs E1 at L3: 6 / 1, p = 0.13). E3/E4 on
fold 0 only, default settings (1 setting tried), L3 of 42 images: E3 database 88.1, E3 head 95.2, E4 97.6
(E1 95.2, SVM 97.6 on the same images; no significant differences): `results/compare_20261111_fold0_E1-E4.md`.
E3/E4 all 5 folds (defaults; 1 setting tried) on all 840: E3 database 100 / 100 / 99.5 / 93.8 (all 98.3), E3 head
100 / 100 / 99.5 / 95.2 (98.7), E4 100 / 100 / 99.5 / **97.1** (99.2). Four-way at L3: E4 vs E1 6 / 2 (p = 0.29), E4 vs SVM 2 / 3
(p = 1.0), SVM vs E3 database 10 / 2 (p = 0.039): `results/compare_20261111_all840_E1-E4.md`. On the test recipe the
noisy-copy methods are tied.
**8 diseases + recipe B (11 Nov, Colab):** black gram did not change the old 840 images (all p >= 0.25); black gram
at L3: E4 90.0, SVM 96.7, E1 90.0, frozen 6.7. **On recipe B the methods separate** (L3, old 7 diseases, test ->
recipe B): frozen 40.0 -> 30.5, E1 95.7 -> 67.1, SVM 97.1 -> 78.1, E3 database 92.4 -> 73.8, E3 head 94.3 -> 79.5,
**E4 96.7 -> 85.2**; E4 beats every other method there (vs SVM 28 / 13, p = 0.028; vs E1 44 / 6). The info-richness
gap returns on recipe B (E4 L3: A 95.3 vs B 78.4, Fisher p = 0.0006), mostly jute mosaic (53%).
`results/compare_20261111_8diseases.md`, `results/robustness_20261111_8diseases.md`, PROJECT_HISTORY.md (Week 9).

**Success (updated 11 Nov).** Beating the frozen database (40.0% at L3) and Gemini + references (47.1%) with
McNemar p < 0.05, without losing L0-L1, is still required but no longer enough: E3/E4 must be compared with
the **noisy album** (85.7-95.2% at L3). E1 is the same design as the album's Idea 1, so it should come out
close to 95% and gives this kit per-image noisy-album predictions for McNemar. Report both the "database"
and "head" predictors, group A vs B, noise types, and the reference table (images with no correct
neighbour at L3: frozen 81 of 210, noisy album 2).

**Next experiments (11 Nov update):** noisy album with a different noise recipe (robustness); real phone
photos; Gemini + noisy references at L3; field photos (e.g. PlantDoc) for the PlantVillage-only diseases
(potato, grape); black gram as an extension; fine-tuning (E3) vs the noisy album.

## Repo map

```
CLAUDE.md                  this file            README.md   setup steps for Nabil
configs/default.yaml       every setting (model, folds, epochs, lr, ...); smoke.yaml, vitb16_fast.yaml
src/safecrop/noise.py      the exact noise recipe + random noisy copies for training
src/safecrop/noise_b.py    recipe B: the same 5 noise types made a different way (robustness test) + levelled SSIM
src/safecrop/data.py       manifest, labels, folds, PairDataset (clean + on-the-fly noisy views)
src/safecrop/clip.py       CLIP loading, Step 2 preprocessing, embeddings, partial unfreezing, checkpoints
src/safecrop/evaluate.py   database vote, zero-shot, tables, McNemar, summary.md / runs.csv
src/safecrop/features.py   saved features, cached embeddings, noisy copies
src/safecrop/finetune.py   training loop (cosine head, consistency loss) + fold scoring
scripts/                   check_setup, reproduce_baseline (E0), noisy_database (E1), linear_probe (E2),
                           finetune (E3/E4), compare, smoke_test, pack_for_colab,
                           make_recipe_b + robustness (E7: recipe-B robustness test),
                           add_black_gram (the 8th disease as an extension)
notebooks/colab_gpu_runner.ipynb   runs the scripts on a free Colab T4 (VS Code Colab extension or browser)
notebooks/previous/        earlier Colab notebooks (reference only; they ran on Colab with Drive); the
                           8-11 Nov ones (noisy album, black gram images) are in Colab only, not copied here
data/                      manifest, labels, features, baselines (+ images/ after unzipping)
results/                   run folders + runs.csv (in git, except cache/ and _smoke/)
```

## Commands

```bash
python scripts/check_setup.py                       # environment, data, noise recipe, saved baseline (no GPU)
python scripts/smoke_test.py                        # every script with a tiny random model (~2 min)
python scripts/reproduce_baseline.py                # E0
python scripts/noisy_database.py                    # E1
python scripts/linear_probe.py --set linear_probe.classifier=svm --tag svm      # E2
python scripts/finetune.py --set finetune.folds=[0] --tag try1                   # E3, one fold (168 images)
python scripts/finetune.py --tag final_settings                                  # E3, all 840 images
python scripts/finetune.py --set finetune.epochs=0 --tag sanity                  # must equal the frozen database
python scripts/compare.py results/finetune/<run>/predictions_database.csv        # tables + McNemar
python scripts/pack_for_colab.py                    # dist/safecrop_code.zip for the Colab runner
python scripts/make_recipe_b.py                     # E7: build/check the recipe-B test set (run first on Colab)
python scripts/noisy_database.py --set test_set=recipe_b --tag e1_rb               # any scoring script on recipe B
python scripts/robustness.py --method NAME ORIGINAL.csv RECIPE_B.csv [--method ...] --out results/robustness_<date>.md
python scripts/noisy_database.py --set black_gram=true --tag e1_8d                 # any scoring script, 8 diseases
python scripts/finetune.py --set black_gram=true --set finetune.also_score_recipe_b=true --tag e3_8d   # train once,
                                                    # score the original images AND recipe B (second folder *_rb)
```

**No local GPU?** `python scripts/pack_for_colab.py`, upload `dist/safecrop_code.zip` (and once
`dist/safecrop_test_images_840.zip`) to Nabil's Drive folder
https://drive.google.com/drive/folders/1EB43yD0e2c-kHmsbk46l89na6bvFMeMB (the notebook finds it by
`DRIVE_FOLDER_ID`; the Google account connected to Claude cannot open it, so ask Nabil what is in it). Open
`notebooks/colab_gpu_runner.ipynb` on a Colab T4 (browser: File > Upload notebook; or VS Code), set
`COMMANDS`, run all, sign in when asked; then unzip the returned `results_<date>.zip` into the repo root.
Free Colab GPU time is limited per day: try settings on fold 0 first.

Any setting can be changed per run with `--set key=value` (names in `configs/default.yaml`).
Each run writes `results/<experiment>/<time>_<model>_<tag>/` with `config.yaml`, predictions,
`summary.md`, `metrics.json`; `results/runs.csv` gets one line per method.

## Code conventions

- Python 3.10-3.13, PyTorch + Hugging Face `transformers` (works with 4.57 and 5.x). Device: `auto`
  picks CUDA, then Apple `mps`, then CPU; fp16 autocast only on CUDA.
- Keep the Step 2 preprocessing (`clip.fit_size` + CLIP mean/std) and the database vote unchanged, or the
  numbers stop being comparable.
- Predictions files always have `image, model, pred_label, confidence, top3` (+ `fold`); neighbours files
  `image, rank, ref_image, ref_disease, similarity, clip_model` (the Step 2b notebook reads this format).
- Scripts that use DataLoader workers need `if __name__ == "__main__":` (Mac/Windows start workers by
  re-importing the script). If workers fail, `--set finetune.num_workers=0`.
- Plain-English comments; small functions; new settings go in `configs/default.yaml` with a comment.
- Long runs: print progress per epoch/fold and write files as you go, so a cut-off Colab session loses little.

## Glossary

L0-L3 = clean/mild/medium/severe noise. **Info-rich (A) / info-scarce (B)** = groups from our
Info-Richness Index (papers, labelled photos, Wikipedia words). **Database** = CLIP nearest-photo vote.
**Leave-one-photo-out** = a photo's own versions are never used to judge it. **Step 2** = the three-model
benchmark; **Step 2b** = Gemini with the database's 5 reference photos + descriptions. **Fixed / broken**
= images a new method gets right that the old got wrong / the reverse (the McNemar counts).
**Confident but wrong** = clear enough + confidence >= 0.8 + wrong. **P3/P2/P1** = retake pipelines from L3/L2/L1.

## Timeline

Week 9 (15 Nov): fine-tuned CLIP + SVM results, four-way comparison. Week 10 (22 Nov): real field photos
(incl. black gram), data card, FastAPI back end around the retake loop. Week 11 (29 Nov): React front end,
demo video, final presentations start. Week 12 (6 Dec): final presentation, live demo, 8-page report.
