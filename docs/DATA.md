# Data card: the SafeCrop 840-image noisy test set

## What it is

210 public photos of 7 crop diseases. Each photo is cut to its central square, resized to 224 x 224
(bicubic) and saved as PNG at four levels: L0 clean, L1 mild, L2 medium, L3 severe noise.
840 images in total. Each photo gets **one** noise type at all three levels (42 photos per type), so
every noisy image has a clean partner.

| Disease | Group | Origin | Info-Richness Index | Photos | Source (licence) |
| --- | --- | --- | ---: | ---: | --- |
| Potato late blight | A, info-rich | Foreign | 0.98 | 25 | PlantVillage, lab photos (CC BY-SA 3.0) |
| Apple scab | A, info-rich | Foreign | 0.82 | 30 | AppleLeaf9 (CC BY 4.0) |
| Rice stem borer (dead heart / white head) | A, info-rich | Local | 0.72 | 30 | Mendeley Data hnfjs42d5g, Bangladeshi field photos (CC BY 4.0) |
| Pear leaf spot | B, info-scarce | Foreign | 0.39 | 35 | DiaMOS Plant (CC BY 4.0) |
| Grape leaf blight (Isariopsis leaf spot) | B, info-scarce | Foreign | 0.38 | 30 | PlantVillage, lab photos (CC BY-SA 3.0) |
| Jute mosaic | B, info-scarce | Local | 0.19 | 30 | Harvard Dataverse doi:10.7910/DVN/FJ1DM1 (CC0) |
| Jute dieback | B, info-scarce | Local | 0.08 | 30 | Harvard Dataverse doi:10.7910/DVN/FJ1DM1 (CC0) |

Black gram yellow mosaic (A, local, index 0.65; Mendeley z55yrbmn2d IDBGL, CC BY 4.0): 30 photos (512 x 512
originals), 6 per noise type, noised with the same recipe and seeds in Colab (8-11 Nov) and added to this repo on
11 Nov as an **extension**: `data/images_black_gram/` (120 images) + `data/manifest_black_gram.csv` (its own folds,
6 photos per fold). With it the test set is 960 images, 8 diseases (`--set black_gram=true`). Report black gram
separately from the 840 images above; the 840 files, `data/manifest.csv` and their folds never change.

## Noise recipe (`src/safecrop/noise.py`)

| Our name | Library effect | L1 | L2 | L3 |
| --- | --- | --- | --- | --- |
| Sensor noise | `gaussian_noise` severity 1/3/5 | sigma 0.08 | 0.18 | 0.38 |
| Hand-shake blur | `motion_blur` severity 1/3/5 (random angle -45..45) | radius 10, sigma 3 | 15, 8 | 20, 15 |
| Out of focus | `defocus_blur` severity 1/3/5 | radius 3 | 6 | 10 |
| Low light | our own: Poisson grain at 120 photons, partial brightening, colour fade | 30% light | 12% | 5% |
| Compression | `jpeg_compression` severity 1/3/5 | quality 25 | 15 | 7 |

Effects 1-4 are from `imagecorruptions` 1.1.2 (Hendrycks & Dietterich, ICLR 2019; Apache-2.0), copied
into `noise.py` because the library no longer imports on current Python. Seed of each test image:
`crc32("299/<photo_id>/<noise>/<level>")`. Noise types were dealt out in turn after a seeded shuffle
per disease. Training copies use other seed families (2026+, or random), never 299.

## Recipe B (robustness test, `src/safecrop/noise_b.py`)

The same 240 photos (incl. black gram), noise types, levels and folds, with L1-L3 made a different way:

| Our name | Recipe B effect | L1 | L2 | L3 |
| --- | --- | --- | --- | --- |
| Sensor noise | Poisson shot noise + clumped grey grain + colour blotches | 241 photons | 52 | 11 |
| Hand-shake blur | curved random-walk shake path, even weights, any direction | 13 px path | 30 | 50 |
| Out of focus | Gaussian blur + red/blue fringes (0.2 x sigma) | sigma 1.7 px | 3.7 | 6.6 |
| Low light | Poisson at 200 photons x light, full auto-exposure, Gaussian smoothing (sigma 1), warm cast | 8.3% light | 3.7% | 1.8% |
| Compression | shrink (INTER_AREA), WebP, enlarge (bicubic) | 78% size, q43 | 68%, q27 | 53%, q9 |

Strengths matched to the test images by levelled colour MS-SSIM (see PROJECT_HISTORY.md, Week 9). Seeds:
`crc32("4242/<photo_id>/<noise>/<level>")`. Files: `data/images_recipe_b/L{1..3}/<disease>/...` (720 images,
rebuilt by `scripts/make_recipe_b.py`) and `data/manifest_recipe_b.csv` (960 rows: the original L0 files + recipe B,
image names prefixed `recipe_b/`, with each image's SSIM and fingerprint).

## Files

- `data/images/L{0..3}/<disease>/<photo_id>_<noise or clean>_L<level>.png` - the 840 images (from
  `safecrop_test_images_840.zip`), plus `data/images/metadata.csv` (the original metadata).
- `data/manifest.csv` - the metadata used by the code, plus `fold` (5 folds by photo, made with seed 299:
  diseases exactly balanced, noise types 7-10 photos per fold).
- `data/labels.csv` - 33 options: key, crop, Gemini name, CLIP name, Gemini description, in_test_set, group.
- `data/extra_references/<option>/PlantVillage/*.JPG` + `data/extra_references.csv` - the 240 PlantVillage
  photos used in the fairness tests (30 each: apple cedar rust, apple healthy, apple scab, grape black rot,
  grape esca, grape healthy, potato early blight, potato healthy). Apple scab here is the "other source"
  set of option 4.
- `data/features/clip_vitl14_frozen.npz` - frozen ViT-L/14 features from the notebooks (Colab T4, fp16):
  `images`, `V` (840 x 768), `label_keys`, `T` (33 x 768 text vectors), `extra_images`, `extra_labels`, `X` (240 x 768).
- `data/baselines/*.csv` - per-image predictions of earlier methods (see `data/README.md`).

## Known limits (say these in reports)

- **Style matching.** Each disease comes from a single source, so a model can partly recognise the
  photo style instead of the disease (apple scab with only other-source references: clean accuracy 100% -> 7%).
  Potato and grape are PlantVillage lab photos on plain backgrounds.
- **PlantVillage duplicates.** All 25 potato late blight and all 30 grape leaf blight test photos are
  exact PlantVillage images. Never use PlantVillage potato late blight / grape leaf blight photos for
  training or references. None of the 30 apple scab photos (AppleLeaf9) is in PlantVillage.
- **Synthetic noise**, one problem per photo; real phone photos may combine problems (dark + compressed).
- **Small numbers.** 210 images per level: about +/-7 points chance variation per level and up to
  +/-18 per disease (95% margins). Use McNemar on paired images, not just accuracy gaps.
- Pear photos are 3968 x 2976 originals: small spots get lost at 224 px.
