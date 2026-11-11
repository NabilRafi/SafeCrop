# data/

Do not edit these files: they are the frozen record every new result is compared with.
Put the test images here by unzipping `safecrop_test_images_840.zip` **into this folder**, which creates
`data/images/` (840 PNGs + metadata.csv) and `data/extra_references/` (240 PlantVillage photos).

| File | What it is |
| --- | --- |
| `manifest.csv` | 840 rows: image, photo_id, disease, disease_name, group (A/B), origin, noise, level, severity, fold, source_file |
| `labels.csv` | the 33 options (7 test diseases + look-alikes + healthy) with Gemini descriptions |
| `extra_references.csv` | the 240 PlantVillage extras (path relative to data/, option, closest test photo) |
| `features/clip_vitl14_frozen.npz` | frozen ViT-L/14 features of the 840 images (V), 33 options (T), 240 extras (X) |

## baselines/ (per-image predictions from the earlier Colab notebooks)

All have an `image` column (as in manifest.csv) and `pred_label`; correct = pred_label == disease.

| File | Method | Rows |
| --- | --- | ---: |
| `clip_database_7.csv` | CLIP photo database, frozen ViT-L/14, k = 5, 7 diseases (Step 2) | 840 |
| `clip_zero_shot_33.csv` | CLIP zero-shot, 33 options (Step 2) | 840 |
| `gemini_plain_33.csv` | Gemini 3.5 Flash-Lite, plain, 33 options (answer, confidence, clear_enough) | 840 |
| `gemini_refs_desc_step2b.csv` | Gemini + the database's 5 reference photos + descriptions (Step 2b) | 840 |
| `gemini_desc_only_L2L3.csv` | Gemini + descriptions only, L2 and L3 | 420 |
| `clip_database_neighbours.csv` | the 5 voting photos per image (image, rank, ref_image, ref_disease, similarity, clip_model): what Step 2b showed Gemini | 4,200 |
| `fairness_all_predictions.csv` | fairness options 1-4: every condition x image (option, condition, choices, draw, correct, ...) | 34,183 |
| `l3_variants_clip.csv` | CLIP database on ~20 edited versions of each L3 photo (variant, pred, correct, chosen) | 8,820 |
| `l3_variants_gemini.csv` | plain Gemini on 4 edited versions of 85 L3 photos | 425 |
| `photo_check_quality_measurements.csv` | the 16 photo-quality measurements of every image | 840 |
| `loop_v2_clip_levels_alone.csv` | retake loop v2: CLIP per level and angle (pred, conf, score, confident) | 3,360 |
| `loop_v2_clip_pipeline_steps.csv` | retake loop v2: every pipeline step (P3/P2/P1, carried or not) | 4,732 |
