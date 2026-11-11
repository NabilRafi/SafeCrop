# SafeCrop – Step 2 inference setup (CLIP + Gemini Flash)

Written 17 Oct 2026. Notebook: `SafeCrop_inference_CLIP_Gemini.ipynb` (Google Colab).

## Dataset used
- `noisy_images.zip`, 840 images: 210 photos × 4 levels (L0 clean, L1 mild, L2 medium, L3 severe). One noise type per photo: sensor noise, hand-shake blur, out of focus, low light, compression.
- 7 diseases:
  - Group A (info-rich): apple scab, potato late blight, rice stem borer.
  - Group B (info-scarce): grape leaf blight, pear leaf spot, jute mosaic, jute dieback.
- Black gram yellow mosaic has no photos yet.
- Potato late blight was missing from the team's first noisy set. Its photos sit in a nested folder (`potato_late_blight_25/`), which the noise notebook skipped.
  - The 100 potato images were added with the same pipeline and seed. The other 740 images reproduce exactly (max difference: 1 grey level).
  - The noise notebooks now also read photos in nested subfolders.

## Predictors
- **CLIP zero-shot** (`openai/clip-vit-large-patch14`)
  - Picks from 33 options: the 8 SafeCrop diseases, same-crop look-alikes, and "healthy" for each crop.
  - Uses names only (no symptom descriptions), so the result reflects what the model already knows.
- **CLIP photo database**
  - The 5 most similar clean (L0) photos of other plants vote; the photo's own clean version is never used (leave-one-photo-out).
  - Chooses among the 7 dataset diseases.
- **Gemini Flash**
  - Gets the same 33 options and returns structured JSON: diagnosis, confidence, and clear_enough (a retake signal).
  - Model is picked automatically: gemini-3.8-flash first, then fallbacks.
  - Paced at about 8 requests per minute and resumable. Answers are cached in `SafeCrop/results/gemini_predictions.csv`.

## Why 33 options
All target diseases except the two jute ones are on different crops. A 7-way choice would mostly test crop recognition; the look-alikes make it a real disease test.

## Outputs (`My Drive/SafeCrop/results`)
- Figures:
  - `table1_accuracy_by_level.png`
  - `table2_info_rich_vs_scarce.png`
  - `table3_by_disease.png`
  - `table4_by_noise_type.png`
  - `chart_accuracy_vs_noise.png`
- `results_tables.xlsx`: also covers local vs foreign, crop accuracy, error types and Gemini retake answers.
- All predictors are compared on the same images; a partial Gemini run uses only the images it has answered.

## Caveats to state in updates
- About ±7 percentage points of chance variation per level, and ±15 per disease.
- Pear photos (3968×2976) lose small spots at 224 px.
- Sources differ by disease (PlantVillage lab photos for potato and grape), so the database method can partly match photo style rather than disease. The field-trip photos (20–22 Oct) will give a fairer test.
- SVM is not run yet.
