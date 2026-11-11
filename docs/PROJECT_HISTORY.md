# SafeCrop: what has been done so far (Weeks 2-9, to 11 Nov 2026)

All accuracies are % correct on the 840-image test set (210 photos x L0-L3) unless a smaller set is named.
Black gram yellow mosaic (added 8-11 Nov) is reported separately.
"Fixed / broken" = images the new method gets right that the old one got wrong / the reverse;
p = McNemar exact test. Per-image predictions for most of these are in `data/baselines/`.

## Team, course and links

- CSE299 Junior Design, North South University, Fall 2026, Section 13, Group 7. Supervisor: Md. Salman Shamil.
  Nabil (Mohammad Nabil Ferdous, ID 2423275042) leads the experiments; teammates own other parts.
- Track 3 (ML model and dataset development): compare a traditional method, a fine-tuned model and a
  zero-shot LLM API, and test on new or changed data.
- Weekly updates: Google Slides deck "Three Project Ideas"
  (https://docs.google.com/presentation/d/1KkVdkICk_VG6YZ4rQ4t9wxhNECiaVwDXkRA84GV755U/edit), Sunday classes.
- Colab notebooks (shared folder "Colab Notebooks": https://drive.google.com/drive/folders/1AaxAU0TmKNfnX91Npf2VMP0BXc1YowJ6):
  inference (Step 2) https://colab.research.google.com/drive/1MGAM3DckhtF0a08q17UCe_D_JG8p0q4H ;
  retake loop v2 https://colab.research.google.com/drive/1eFHy3ro_0QiGb2fVCTGxtHoLnJrnUGMc ;
  Gemini with references (Step 2b) https://colab.research.google.com/drive/1X4NCj9r8YE-jR-ysaoRPBQZHp7JzzFqj ;
  fairness options https://colab.research.google.com/drive/1ifXLDTCue4BxHVsffYPMD7bAMYh4Vv5m ;
  L3 variants https://colab.research.google.com/drive/1pPkbLjj5xMZX431Oh3McpyqHoqdrylxs ;
  photo check https://colab.research.google.com/drive/1xqokLaDZaw_J0ulX5N3n48J3gvUFdoHo .
  Copies are in `notebooks/previous/`.
- Dataset folder (Google Drive): https://drive.google.com/drive/folders/1q3rB5OeE9UBq9kQnvbbMCx996hbczyhh

## Weeks 2-4: question and disease groups

- Week 2: assigned to Track 3. Supervisor's advice: study two axes, **image clarity** and **how well-studied
  a disease is**. The earlier idea (a CLIP out-of-distribution gate with NegLabel/TANL) was dropped.
- Week 4 (9 Oct): **Info-Richness Index** (0-1) = mean of log(1 + count) of research papers (OpenAIRE),
  labelled public photos and Wikipedia words, rescaled over 20 candidate diseases.
  Group A (info-rich): potato late blight 0.98, apple scab 0.82, rice stem borer 0.72, black gram yellow
  mosaic 0.65 (photos added 8-11 Nov, see Week 9). Group B (info-scarce): pear leaf spot 0.39, grape leaf blight 0.38, jute
  mosaic 0.19, jute dieback 0.08. Matched pairs (same symptom type and photo style): potato late blight vs
  grape leaf blight; apple scab vs pear leaf spot; rice stem borer vs jute dieback; black gram yellow mosaic
  vs jute mosaic.

## Week 5 (17 Oct): test set and the three-model benchmark (Step 2)

- 210 public photos, each cut to its central square, resized to 224 x 224, one noise type per photo
  (42 each), saved at L0-L3 with a fixed seed (299). See `docs/DATA.md`.
- Predictors (all on the same 840 images):
  - **CLIP zero-shot** (ViT-L/14): closest of 33 options (4 sentences each, averaged), names only.
  - **CLIP photo database**: the 5 most similar clean photos of other photos vote (cosine-weighted), 7 diseases.
  - **Gemini** (3.8 Flash in Weeks 5-6; 3.5 Flash-Lite from Week 7 on the free key): same 33 options, JSON
    answer with diagnosis, confidence, clear_enough.

| Predictor | L0 | L1 | L2 | L3 | All | A | B |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CLIP database | 100 | 93.3 | 71.9 | 40.0 | 76.3 | 81.2 | 73.0 |
| Gemini 3.5 Flash-Lite, 33 options | 66.7 | 48.6 | 26.2 | 12.9 | 38.6 | 54.7 | 27.6 |
| CLIP zero-shot, 33 options | 25.7 | 15.2 | 8.6 | 3.8 | 13.3 | | |

- At L3: database A 48% vs B 34%; Gemini A 29% vs B 2%. Zero-shot gets 0% on clean apple scab, rice and jute.
- Errors (share of 840 answers): wrong crop is the biggest error for all (database 22%, Gemini 28%,
  zero-shot 47%). Gemini's most common L3 answer: "Apple: healthy" (61 of 210).
- By noise (L1-L3, database): compression 78%, hand-shake blur 71%, low light 71%, out of focus 62%,
  sensor noise 61%. Gemini's worst: low light (19%).
- Gemini's "clear enough" flag is informative: right 1.6-3x as often when it says clear. Run-to-run it gave
  the same answer 63-68% of the time.
- By disease (database clean / noisy): potato 100/77, apple scab 100/48, rice 100/100, pear 100/70,
  grape 100/94, jute mosaic 100/58, jute dieback 100/33. Gemini called clean jute mosaic "jute anthracnose"
  24 of 30 times.

## Weeks 6-7 (25 Oct - 1 Nov): the retake loop

- v1: start at L3; if not confident, show the same photo one level clearer. CLIP stop rule qc >= 0.8
  (logistic regression on 8 photo-quality features + CLIP confidence, out-of-fold): 40.0% -> 88.6% with
  2.40 photos on average (own-confidence stop rule: 68.1%, 31.9% confident but wrong).
- v2 (supervisor's review): each level judged alone (CLIP L0-L3 99.9 / 90.8 / 68.5 / 38.5 over 4 angles),
  pipelines P3/P2/P1 that carry the previous level's features, at 4 angles (original, rot90, rot180,
  mirror). P3: 2.59 photos, 87.7% (nothing carried: 2.52, 91.0%). **Carrying features always hurt**
  (P3 L3->L2 step: 48.7% vs 62.7% judged alone). Angles change accuracy by at most 7.6 points.
- Gemini 3.5 Flash-Lite in the loop: L3 alone ~15%; the loop lifts it to ~51% but it often stops on a
  confident wrong answer.
- Mid-project report submitted 1 Nov. Supervisor's feedback: a farmer's phone may only ever give
  L3-quality photos, so keep the level fixed and try variants (L3 -> L3' -> L3''); improve Gemini with a
  "prompt option" or "visual similarity"; use each level's judged-alone accuracy as the benchmark.

## Week 8 (2-8 Nov)

### Step 2b: Gemini + the database's 5 reference photos + descriptions (all 840)

| Predictor | L0 | L1 | L2 | L3 | All | A | B |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Gemini + references + descriptions | 100 | 92.9 | 75.2 | 47.1 | 78.8 | 80.6 | 77.6 |
| CLIP database | 100 | 93.3 | 71.9 | 40.0 | 76.3 | 81.2 | 73.0 |

- vs database: all 33 fixed / 12 broken (p = 0.003); L3 18 / 3 (p = 0.002); L2 12 / 5 (p = 0.14).
  vs plain Gemini: 353 / 15. L3 A 48.2 vs B 46.4: the info-scarce gap closes (19 of the 33 fixes are jute mosaic).
- It follows the references: label among the references 98.6%, the most similar photo's label 91%.
- By number of the 5 references that show the true disease (images; Gemini+refs right; database right):
  0 (123; 1; 0), 1 (44; 12; 0), 2 (57; 41; 25), 3 (55; 49; 55), 4 (66; 65; 66), 5 (495; 494; 495).
  **At L3, 81 of 210 images have no correct reference** - the ceiling for any reference method.
- Confident but wrong (L0-L3): with references 0 / 4 / 4 / 7% vs plain 32 / 34 / 20 / 13%.
- Descriptions only (no photos), L3: 18.1% (vs plain 12.9%: 16 / 5, p = 0.03); L2 31.0% (p = 0.14).
  So of the 34-point L3 gain, ~5 points come from descriptions and ~29 from photos; descriptions help
  info-rich (rice stem borer 57 -> 87%) but not info-scarce (3%).

### Fairness tests (is the database's lead fair?)

- Same 7 choices (L3): plain Gemini 41.0% (62 fixed / 3 broken vs 33 choices) = database 40.0% (35 vs 33,
  p = 0.90). CLIP zero-shot with 7 choices: L3 25.2%, all levels 44.8%.
- Database filled with 240 PlantVillage photos (4 look-alike diseases + 3 healthy leaves): L0-L3
  99.5 / 86.7 / 46.2 / 15.2%. At L3: 73% of photos called a healthy leaf; look-alikes only 32%, healthy only 16%.
  Gemini with references from the filled database: 20.5% at L3 (still beats that database 14 vs 3, p = 0.01).
- k clean photos per disease (10 random draws), L3: 1 photo 34.6%, 3 33.8%, 10 38.4%, all 40.0%.
  Gemini + 1 photo per disease + descriptions at L3: 40.4% vs database with the same photos 31.0% (45 vs 26, p = 0.03).
- Apple scab only, references from other datasets: clean 100% -> 7% (database partly matches photo style).

### L3 variants (fixed-L3 direction) and photo check

- ~20 edited versions of each L3 photo (brighten, gamma, CLAHE, contrast, denoise, sharpen, resample,
  deblock, white balance, zoom, combinations): none beats the photo as taken overall (database 40.0%):
  brighten 38.1 (3 / 7), resample 41.4 (16 / 13), CLAHE 31.4, denoise 28.6, **zoom 19.0 (0 fixed / 44 broken)**.
- By noise type, only compression -> resample is proven: 57 -> 79% (9 / 0). Fix chosen per detected
  problem (learned out-of-fold): 40.0 -> 47.1% (16 / 1, p < 0.001), mostly from compression.
- Retry pipelines (stop at vote share >= 0.8) never beat one try (CLIP 29.5-38.1% vs 40.0%; best possible 42.9%).
- Photo quality check (16 measurements + random forest, 5 folds by photo): problem type right 97.7%,
  level right 92.0% (99.6% within one level); weak spots: dark photos without grain, JPEG quality 80.
  Not yet tested on real photos. App flow: check -> resample if compressed -> diagnose.

### Gemma 4 31B (dropped)

- 180 images (45 photos x 4 levels): Gemma 25.6% vs plain Gemini 38.9% (13 vs 37, p = 0.0009); free API
  very slow (~75 s per image, many server errors).

### k-means quick tests (6 Nov, saved features, not yet cross-validated)

- Frozen L3 embeddings cluster by **noise type** (adjusted Rand index 1.00), not disease (-0.02).
- 3 reference photos per disease picked at k-means centres: L3 43.8% (random 3 photos: 32-40%).

### App UI

- 4 design directions drafted (6 Nov); one to be picked. Planned flow: photo check -> resample ->
  Gemini + references (and/or fine-tuned CLIP) -> answer or ask for a clearer photo.

## Week 9 starting point (this repo, 8 Nov)

- Kit checks: the saved frozen features reproduce the Step 2 database and zero-shot predictions 840/840;
  the noise code rebuilds the test images (612/630 identical, the rest within 1 grey level).
- Clean-only classifiers on frozen features (5 folds by photo, C chosen inside training photos):
  logistic probe 99.5 / 92.4 / 57.1 / 26.2 (all 68.8); RBF SVM 100 / 92.4 / 74.3 / 37.1 (all 76.0;
  A 80.6, B 72.8). SVM vs database: 23 vs 26 (p = 0.78); L3 9 vs 15 (p = 0.31).
- Week 8 "next steps" slide: noisy copies in the reference database; noisy healthy photos + a "can't tell"
  answer for Gemini; k-means reference choice (3-5 per disease); photo check on 20-30 real phone photos;
  pick an app UI direction.
- Remaining plan: Week 9 fine-tuned CLIP + SVM + four-way comparison; Week 10 field photos (incl. black
  gram), data card, FastAPI back end; Week 11 React front end, demo video; Week 12 final presentation,
  live demo, 8-page report.

## Week 9 (8-11 Nov): noisy reference album and black gram

### Noisy reference album (supervisor's advice: compare noisy photos with noisy photos)

- Colab notebook `SafeCrop_noisy_album_idea2.ipynb` (not copied into this repo yet). Every album photo
  (our 210 + 210 PlantVillage healthy / look-alike leaves) gets 15 noisy copies (5 noise types x L1-L3,
  seed family 2026, never 299); leave-one-photo-out; same ViT-L/14 and k = 5 vote as Step 2.
- Idea 1 = one mixed album (clean + all copies). Idea 2 = a separate album per noise type + level; the
  photo check (random forest: type 97.7%, level 92.1% right) picks the album.

| L3 (210 images) | Frozen, clean only | Idea 2 | Idea 1 | No correct neighbour at L3 |
| --- | ---: | ---: | ---: | ---: |
| Our 7 diseases | 40.0 | 93.8 | 95.2 | 81 -> 2 |
| Filled album (+ healthy / look-alike leaves) | 15.2 | 85.7 (151 fixed / 3 broken) | 88.1 | 151 -> 6 |

- Filled album: "called healthy" at L3 73% -> 5%; L0 unchanged at 99.5%. Both ideas beat Gemini +
  references (47.1%).
- The noisy copies do the work, not the matching: Idea 1 is as good or better and doesn't need the photo check.
- Info-rich vs info-scarce at L3 (Idea 2): filled 81.2 vs 88.8; our 7: 94.1 vs 93.6. The gap disappears;
  the flip comes from potato's PlantVillage overlap and is not significant.
- Caveats: photo style (one dataset per disease): potato (56%) and grape (77%) share PlantVillage style
  with the extras, so they are the fair check. The album uses the same noise recipe as the test set, so
  this is a best case.
- Section 9 of the notebook tests uploaded photos. The first real field photo (potato late blight) was
  answered "apple scab" with 100% of the vote by all three albums, because the album only has PlantVillage
  lab photos of potato. Next: add field photos (e.g. PlantDoc) for the PlantVillage-only diseases
  (potato, grape).
- Note: the Week 8 filled database (15.2%) had 240 PlantVillage photos (`data/extra_references.csv`):
  7 look-alike / healthy classes x 30 = 210, plus 30 PlantVillage apple scab.

### Black gram yellow mosaic added

- 30 clean photos (512 x 512). Group A (info-rich), Local, index 0.65; 6 photos per noise type. The test
  set is now **960 images = 240 photos x 4 levels, 8 diseases**.
- Colab notebook `SafeCrop_make_noisy_images_with_black_gram.ipynb`: same recipe and seeds. The noise code
  is copied into the notebook (`imagecorruptions` no longer installs on Colab). It only reads zips with
  "clean" in the name.
- The old 840 images are unchanged (821 identical, 19 within 1 grey level), so existing results stay valid.

### What this means for this repo

- `data/manifest.csv`, the 5 folds, saved features and baselines still cover the 840 images / 7 diseases.
  Don't overwrite them. Add black gram as an extension: new rows plus folds for its 30 photos, balanced by
  noise type, keeping the old 210 photos' folds as they are.
- Report the old 7 diseases and black gram separately, so earlier numbers (40.0% at L3 etc.) stay comparable.
- Next experiments: noisy album with a different noise recipe (robustness); real phone photos; Gemini +
  noisy references at L3; field photos for potato / grape; fine-tuning (E3) compared with the noisy-album
  baseline (85.7-95.2% at L3), not just 40%.

### This repo: E0-E4 (11 Nov)

- E0 (Nabil's laptop, CPU, ~50 min): frozen ViT-L/14 recomputed from the images gives exactly the Step 2
  numbers (database 100 / 93.3 / 71.9 / 40.0, all 76.3; zero-shot 25.7 / 15.2 / 8.6 / 3.8); 0 of 840 answers
  changed. No correct neighbour: 81 at L3, 122 over all levels (the Step 2b count was 123).
- E1 (Colab T4): frozen CLIP + 3,150 noisy copies (5 types x L1-L3, seed 2026) in the database,
  leave-one-photo-out: 100 / 100 / 99.0 / **95.2**, all 98.6 (A 98.8, B 98.4; L3: A 95.3, B 95.2). Same L3
  result as the Colab album's Idea 1. vs frozen database: L3 120 fixed / 4 broken, all 192 / 5; vs Gemini +
  references: L3 106 / 5, all 172 / 6 (all p < 0.001). L3 by noise: sensor noise 85.7, hand-shake blur 100,
  out of focus 95.2, low light 100, compression 95.2. No correct neighbour at L3: 1 of 210. Share of the
  5 neighbours that are copies: L0 4%, L3 100%.
- Only 10 L3 images (12 over all levels) are still wrong, so on these 840 images a fine-tuned model can
  hardly show a significant win over E1 (it would have to fix at least 6 of the 10 L3 errors and break
  none). Its real test is a different noise recipe and real photos.
- Sanity check (fold 0, 0 epochs): the fine-tuning code without training gives exactly the frozen
  database's answers (0 fixed / 0 broken on 168 images).
- E2, RBF SVM on frozen features trained on clean + noisy copies of the training photos (5 folds; C per fold
  100 / 10 / 1 / 10 / 100, chosen inside the training photos): 100 / 99.5 / 99.0 / **97.6**, all 99.0
  (A 99.4, B 98.8). vs frozen database: L3 123 / 2, all 194 / 3; vs Gemini + references: L3 108 / 2,
  all 173 / 3 (all p < 0.001). vs E1: L3 6 / 1 (p = 0.13), all 7 / 3 (p = 0.34): not significant.
- E3 / E4, fine-tuned with the default settings (last 4 blocks, 15 epochs, lr 1e-5, consistency 1.0),
  fold 0 only (168 images; ~100 s per fold on a T4, E4 ~170 s). L3 % correct on fold 0 (42 images): frozen
  database 35.7, E3 database 88.1, E3 head 95.2, E1 95.2, E2 SVM 97.6, E4 database 97.6; L0-L2 100% for
  E3 / E4. vs frozen database at L3: E3 head 25 / 0, E4 26 / 0 (p < 0.001). vs E1 at L3: E4 1 / 0, E3 head
  1 / 1, E3 database 1 / 4 (all p >= 0.375): no difference. One L3 image (jute_dieback_026, compression) is
  wrong for every method. Settings tried so far: 1 (defaults). Tables: `results/compare_20261111_fold0_E1-E4.md`.
- Fine-tuning alone (E3 database, clean references) is weaker than simply adding noisy copies (E1);
  fine-tuning + noisy copies (E4) gives the best number, but within 1-2 images of E1 and the SVM. On this
  test set the methods can no longer be told apart.
- E3 / E4, all 5 folds (default settings; ~95 s per fold, E4 ~160 s, Colab T4), all 840 images:

| Method (all 840) | L0 | L1 | L2 | L3 | All | A L3 | B L3 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Frozen database (Step 2 = E0) | 100 | 93.3 | 71.9 | 40.0 | 76.3 | 48.2 | 34.4 |
| Gemini + references (Step 2b) | 100 | 92.9 | 75.2 | 47.1 | 78.8 | 48.2 | 46.4 |
| E1 frozen + noisy copies | 100 | 100 | 99.0 | 95.2 | 98.6 | 95.3 | 95.2 |
| E2 SVM, frozen + noisy copies | 100 | 99.5 | 99.0 | 97.6 | 99.0 | 97.6 | 97.6 |
| E3 fine-tuned, database | 100 | 100 | 99.5 | 93.8 | 98.3 | 95.3 | 92.8 |
| E3 fine-tuned, head | 100 | 100 | 99.5 | 95.2 | 98.7 | 95.3 | 95.2 |
| E4 fine-tuned + noisy copies | 100 | 100 | 99.5 | 97.1 | 99.2 | 97.6 | 96.8 |

  vs frozen database at L3: E3 database 114 / 1, E3 head 117 / 1, E4 121 / 1 (all p < 0.001). Among the
  noisy-copy methods at L3: E4 vs E1 6 / 2 (p = 0.29), E4 vs SVM 2 / 3 (p = 1.0), E3 head vs E1 6 / 6, SVM vs E3
  database 10 / 2 (p = 0.039, the only significant difference). Tables: `results/compare_20261111_all840_E1-E4.md`.

### Black gram yellow mosaic added to this repo (11 Nov)

- `scripts/add_black_gram.py` copied the 120 images (30 photos x L0-L3) into `data/images_black_gram/` and wrote
  `data/manifest_black_gram.csv`. Recipe check against noise.py with the test seeds: 88/90 noisy images identical,
  90/90 within 1 grey level. Own folds: 6 photos per fold, every noise type in every fold (seeded shuffle, 299).
  The 840 original files, `data/manifest.csv` and their folds are unchanged.
- The code takes `--set black_gram=true` (8 diseases, 960 images; 8-way head; references and noisy copies of all
  240 photos). Reports show the 840 original images first, then black gram only, then all 960.

### Recipe B: a second noisy test set for robustness (E7, built 11 Nov)

- Why: on the test recipe E1, E2 and E4 are 1-2 images apart at L3, so that test set can no longer separate
  them, and every method learned the test recipe's own noise. Recipe B keeps the 240 photos (incl. black gram),
  noise types, levels and folds, and makes the noise a different way (`src/safecrop/noise_b.py`):

| Noise | Test recipe | Recipe B | B strength L1 / L2 / L3 |
| --- | --- | --- | --- |
| Sensor noise | even Gaussian grain per pixel and colour | grain that grows with brightness, clumped, + colour blotches | 241 / 52 / 11 photons |
| Hand-shake blur | straight line, -45..45 degrees | curved shake path, any direction | 13 / 30 / 50 px path |
| Out of focus | sharp-edged disk | Gaussian blur + colour fringes | sigma 1.7 / 3.7 / 6.6 px |
| Low light | darker, grainy, faded | auto-brightened very noisy dark photo, smoothed, warm cast | 8.3% / 3.7% / 1.8% light |
| Compression | JPEG 25 / 15 / 7 | shrink, WebP, enlarge | 78% size q43 / 68% q27 / 53% q9 |

- Strength matched per noise type and level to the test images (same 42 photos each; no model, no labels) by
  levelled colour MS-SSIM: SSIM at 5 scales, per colour channel, after matching each channel's brightness and
  contrast to the clean photo. Every level within 0.001 (calibration seeds 5005; images seeds 4242).
  Three simpler rules were tried and dropped BEFORE anything was scored on recipe B, each after looking at the
  images: plain grey SSIM (it counts a photo as damaged just for being dark, so B's low light came out far
  harsher), levelled grey SSIM (it barely sees colour grain) and levelled colour SSIM (single scale: fine grain
  counts as heavy damage but blotches hardly count, so B's blotchy sensor noise and low light came out harsher).
  With MS-SSIM the low-light and blur rows look comparable by eye; B's sensor noise at L3 still looks a little
  rougher than the test images'.
- `data/manifest_recipe_b.csv` (960 rows) + `data/images_recipe_b/` (720 images); score any script with
  `--set test_set=recipe_b`; `scripts/robustness.py` makes the test-recipe vs recipe-B tables.

### 8 diseases + recipe B results (Colab T4, 11 Nov; default settings, 1 setting tried)

All runs with black gram as an 8th choice (960 images). Tables: `results/compare_20261111_8diseases.md`,
`results/robustness_20261111_8diseases.md`. Fine-tuning trained once per fold and scored both test sets. Colab
rebuilt recipe B with 633 of 720 noisy images bit-identical to the local set (the rest differ slightly, most likely
library versions; the scores use Colab's images, which were not kept).

- **Black gram did not change the old 840 images:** every method within 3 images of its 7-disease run (all
  p >= 0.25); at most 4 old images were called black gram. Black gram itself, L0 / L1 / L2 / L3 (30 images each):
  frozen database 100 / 66.7 / 20.0 / 6.7; E1 100 / 96.7 / 86.7 / 90.0; SVM 100 / 100 / 100 / 96.7; E3 database
  100 / 96.7 / 93.3 / 80.0; E3 head 100 / 96.7 / 96.7 / 93.3; E4 100 / 96.7 / 96.7 / 90.0. Its misses are mostly
  "jute mosaic" (its matched yellow-mosaic pair). CLIP zero-shot gets 0% of clean black gram.

| L3, old 7 diseases (210 images) | Test recipe | Recipe B | Change (paired McNemar: only B right / only test right) | Recipe B: A vs B |
| --- | ---: | ---: | --- | --- |
| Frozen database | 40.0 | 30.5 | -9.5 (8 / 28, p = 0.001) | 41.2 vs 23.2 |
| E1 frozen + noisy copies | 95.7 | 67.1 | -28.6 (5 / 65, p < 0.001) | 75.3 vs 61.6 |
| E2 SVM + noisy copies | 97.1 | 78.1 | -19.0 (4 / 44, p < 0.001) | 88.2 vs 71.2 |
| E3 fine-tuned, database | 92.4 | 73.8 | -18.6 (7 / 46, p < 0.001) | 90.6 vs 62.4 |
| E3 fine-tuned, head | 94.3 | 79.5 | -14.8 (5 / 36, p < 0.001) | 90.6 vs 72.0 |
| E4 fine-tuned + noisy copies | 96.7 | **85.2** | -11.5 (5 / 29, p < 0.001) | 95.3 vs 78.4 |

- **On recipe B the methods separate.** At L3, E4 beats E1 (44 / 6, p < 0.001), the SVM (28 / 13, p = 0.028), E3 head
  (19 / 7, p = 0.029) and E3 database (24 / 0); all levels E4 vs SVM 36 / 20 (p = 0.044). SVM beats E1 (34 / 11);
  SVM = E3 head (18 / 21, p = 0.75). Black gram at L3 on recipe B (30 images): E4 76.7, E3 head 73.3, SVM 70.0,
  E3 database 63.3, E1 20.0, frozen 0.
- So fine-tuning (with noisy copies) is the most robust to noise made a different way, and noisy copies alone (E1)
  had partly learned the test recipe itself (the largest drop). The frozen database's own drop (-9.5) shows recipe
  B is somewhat harder overall. Recipe B, E4 at L3 by noise: sensor noise 64.3, hand-shake 92.9, out of focus 85.7,
  low light 85.7, compression 97.6 (E1: 54.8 / 76.2 / 64.3 / 69.0 / 71.4).
- **The info-richness gap comes back on recipe B:** at L3, E4 group A 81/85 = 95.3% vs group B 98/125 = 78.4%
  (Fisher p = 0.0006; SVM p = 0.004; frozen p = 0.006; E1 p = 0.051); on the test recipe it was gone (p = 1.0).
  Mostly jute mosaic (E4: 100% -> 53% at L3; misses: apple scab 6, black gram 6, pear 2; mostly sensor noise and
  low light, recipe B's blotchy-colour types); pear leaf spot 94 -> 80, grape 100 -> 87. Caveats: one photo source
  per disease (A vs B is confounded with disease and source), small numbers per disease, and recipe B's sensor
  noise at L3 looks a little rougher than the test images'.
