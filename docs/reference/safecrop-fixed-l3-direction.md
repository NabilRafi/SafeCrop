# SafeCrop – Week 7 feedback: fixed-L3 direction (1 Nov 2026, updated 6 Nov)

## Supervisor feedback (Week 7 class)
- Improve Gemini with a "prompt option" or "visual similarity" (exact meaning still to confirm with the supervisor).
- Realistic case: a farmer's phone only ever gives L3-quality photos, so a clearer L2 photo is not available. Keep the level fixed, make variants (L3 → L3′ → L3″ by angle and other changes) and try to reach the right answer after a few tries.
- Use each level's "judged alone" accuracy as the benchmark to beat.

## What the existing data says (computed 1 Nov from the loop v2 CSVs)
CLIP photo database, 210 photos, views = original, rot90, rot180, mirror:

| Level | Original photo alone | Vote of 4 views | Stop at first confident view (avg tries) | Any of the 4 views right (best possible) |
| --- | --- | --- | --- | --- |
| L3 | 40.0% | 38.1% | 38.1% (3.2) | 48.1% |
| L2 | 71.9% | 71.0% | 71.9% (2.5) | 79.0% |
| L1 | 93.3% | 93.3% | 93.8% (1.5) | 96.7% |

- At L3, all 4 views gave the same answer for 73% of photos: rotating or mirroring the same noisy photo adds no new information.
- Gemini asked twice on the same L3 images: 12.9% and 14.8% correct; same answer 52% of the time; either run right 18.1% (best possible from re-asking).
- In the loop run, 68% of Gemini's L3 answers were some crop's "healthy" (no test photo is healthy). Its notes often say the image is too dark or noisy to see.

## Step 2b result: Gemini with the database's reference photos (final, all 840 images, 3 Nov)
- Explainer: SafeCrop_gemini_with_references_explained_3Nov2026.pdf (8 pages, same style as the 30 Oct inference explainer).
- Accuracy L0/L1/L2/L3/all: Gemini + references + descriptions 100/92.9/75.2/47.1/78.8%; CLIP database 100/93.3/71.9/40.0/76.3%; plain Gemini 66.7/48.6/26.2/12.9/38.6%; CLIP zero-shot 25.7/15.2/8.6/3.8/13.3%.
- Versus the database (McNemar): all levels 33 fixed, 12 broken, p = 0.003; L3 18 vs 3, p = 0.002; L2 12 vs 5, p = 0.14; L0 and L1 the same. Versus plain Gemini: 353 fixed, 15 broken.
- Info-rich vs info-scarce: plain Gemini 54.7% vs 27.6%; with help 80.6% vs 77.6% (L3 48.2% vs 46.4%); database 81.2% vs 73.0%. Info-rich: help = database; all of the lead is on info-scarce. Jute mosaic noisy 2% (plain) → 78% (help) vs 58% (database); 19 of the 33 fixes over the database are jute mosaic.
- Noise types (L1–L3), help vs database: hand-shake blur 79 vs 71, compression 84 vs 78, out of focus 66 vs 62, sensor noise 61 vs 61, low light 69 vs 71.
- It follows the references: agrees with the database 89% (L3 77%); answers with a label shown in the references 98.6%, the most similar photo's label 91%. By number of the 5 references showing the true disease (images; help right; database right): 0 (123; 1; 0), 1 (44; 12; 0), 2 (57; 41; 25), 3 (55; 49; 55), 4 (66; 65; 66), 5 (495; 494; 495). At L3, 81 of 210 images have no right reference: a ceiling for any reference-based method.
- Confidence: confident but wrong (clear enough + confidence ≥ 0.8 + wrong) L0–L3: help 0/4/4/7% vs plain 32/34/20/13%. Help says clear enough 100/94/57/22%; right when clear 100/95/92/70%.

## Descriptions only, no reference photos (4 Nov, L3 only, 210 images)
- L3 accuracy: descriptions only 18.1% vs plain 12.9% (16 fixed, 5 broken, p = 0.03) vs photos + descriptions 47.1% (descriptions only lost 68, won 7).
- So of the 34-point L3 gain from Step 2b, about 5 points come from the descriptions and about 29 from the reference photos.
- Info-rich 40.0% (plain 29.4%); info-scarce 3.2% (plain 1.6%): text descriptions do not help the little-studied diseases at L3; the gain is mostly rice stem borer (57% → 87%) and potato late blight (24% → 28%).
- Still answers some crop's "healthy" 42% of the time (plain 48%). Says clear enough 16%; confident but wrong 8% (plain 13%, photos + descriptions 7%).
- Descriptions only at L2: 31.0% (info-rich 60, info-scarce 11.2) vs plain 26.2%, p = 0.14.
- Refines the research conclusion: the info-scarce gap is closed by showing labelled examples, not by describing the disease in words.

## Gemma 4 31B vs plain Gemini (4–5 Nov, 180 of 840 images, 45 photos × 4 levels)
- Same plain prompt and 33 options. Gemma 25.6% vs plain Gemini 38.9% (only Gemma right 13, only Gemini 37, p = 0.0009); L0 40 vs 71%, L3 7 vs 20%. 60% of Gemma's mistakes are the wrong crop. Free Gemma API very slow (many 500 errors). Dropped from the project.

## Fairness notebook results (5 Nov, final; explainer SafeCrop_fairness_results_explained_5Nov2026.pdf, 7 pages)
- Option 1, same choices (L3): plain Gemini 33 → 7 choices 12.9% → 41.0% (62 fixed, 3 broken); equals the CLIP database (40.0%; 35 vs 33, p = 0.90). Of the 62 fixes, 26 had been "healthy", 35 a disease outside our 7. CLIP zero-shot 7 choices: 25.2% at L3, 44.8% all levels. Step 2b vs Gemini 7 choices at L3: 40 vs 27, p = 0.14. L3 info-rich/scarce with 7 choices 54/32%.
- Option 2, database filled with 240 PlantVillage photos (30 each: apple cedar rust, apple healthy, grape black rot, grape esca, grape healthy, potato early blight, potato healthy; 14 options): CLIP database L0/L1/L2/L3/all 99.5/86.7/46.2/15.2/61.9% (L3: 0 fixed, 52 broken). Recomputed from saved features: + look-alikes only 32.4% at L3, + healthy only 16.2%, without apple healthy 21.0%, without all healthy 32.4%. 73% of L3 photos called a healthy leaf (138/210 apple healthy). L3 photos' best CLIP similarity: closest healthy apple 0.72 vs closest own-disease photo 0.68. Rice stem borer survives (77% at L3); apple scab and potato late blight 0%.
- Option 2, Gemini + 5 references from the filled database (L3): 20.5% (vs Step 2b 47.1%: 1 vs 57); says healthy 56%; answer among references 92%; 151 of 210 photos have no right reference (Step 2b 81), 2 of them right; 3.5 of 5 references healthy on average. Still beats the filled database with the same references (14 vs 3, p = 0.01). Info-rich/scarce 36.5/9.6%.
- Option 3, k photos per disease (10 random draws): L3 1/3/5/10/all = 35/34/33/38/40% (1-photo draws range 27–44%); L1 76 → 93%, L2 53 → 72% from 1 photo to all; all levels info-rich 77 → 81%, info-scarce 56 → 73%.
- Option 3, Gemini + 1 fixed photo per disease + descriptions (203 L3 photos): 40.4% vs CLIP database with the same 1 photo 31.0% (45 vs 26, p = 0.03); says healthy 9%; info-rich 65.9%, info-scarce 23.1%; pear leaf spot 0 of 34.
- Option 4, apple scab only (30 PlantVillage apple scab as the other source): examples from any dataset 100/80/27/0% (all 52%); other datasets only 7/33/10/0% (all 13%; 47 broken, 0 fixed); clean photos mostly called pear leaf spot (22/30). L3 0% in both because the filled database's healthy leaves win.
- Conclusions: Gemini uses the same references better than the database in all three settings (Step 2b, filled, 1-photo); Step 2's database-vs-plain-Gemini gap was mostly the 7 vs 33 choices; healthy leaves in the database are the biggest threat at L3 (same "healthy" failure as plain Gemini); the database partly matches dataset style (one disease tested). Limits: Gemini jobs L3 only; extras all PlantVillage; option 4 one disease.

## L3 variants and photo check results (6 Nov, run by Nabil)
- CLIP database at L3 (210 photos, 42 per noise type), accuracy as taken 40.0%. Every single fix applied to all photos was neutral or harmful: brighten 38.1 (3 fixed/7 broken), zoom 19.0 (0/44), brighten+zoom 19.0, gamma 36.2, CLAHE 31.4, contrast 34.3, denoise 28.6, sharpen 30.5, resample 41.4 (16/13), deblock 39.0, white balance 38.1, auto (rules) 32.4.
- Only per-problem win that is proven: compression → resample 57 → 79% (9/0, p < 0.01). Others are small and not proven: hand-shake blur → resample 33 → 40% (4/1), out of focus → white balance 29 → 36% (3/0), grain → white balance 26 → 29%; low light: nothing beats as taken (55%), brightening 43%.
- Auto (learned) = per detected problem, the version that worked best on the other photos (out-of-fold, 5 groups by photo): 47.1% vs 40.0% (16 fixed, 1 broken, p < 0.001); choices were stable (compression → resample, hand-shake → resample, out of focus → white balance, grain → white balance in 36 of 42, low light → none). Without compression it is 7 fixed / 1 broken (p = 0.07).
- Zoom hurts everything (−20 points): the database compares with un-zoomed clean photos, and enlarging an L3 photo enlarges its noise. Zoom also raised "confident but wrong" in the pipelines (30% → 54%).
- CLIP zero-shot stays at 0.5–5% for every version.
- Gemini (plain, 85 L3 photos = 17 per noise type): as taken 14.1%, brighten 17.6% (4/1, p = 0.38), auto (rules) 17.6% (7/4), zoom 5.9% (1/8, p = 0.04).
- Retry pipelines (stop at vote share ≥ 0.8) don't beat a single try: CLIP 40.0 → 29.5–38.1%, Gemini 14.1 → 7.1–17.6%; best possible (any try right) at most 42.9% (CLIP) and 20.0% (Gemini).
- Conclusion: image fixes can't put back disease detail that L3 noise has erased; the only robust gain is removing JPEG blocks.
- Photo check notebook (Nabil's edit): ROUTE hard-coded so only compression gets a fix (resample); best_fix_per_problem.csv no longer read. Six built-in examples (5 L3 of one photo each + 1 clean) all got the right problem and level (main problem 78–100% sure); the clean potato photo got a borderline "grainy" warning (0.0358 vs normal up to 0.0347) while the forest said clean 99%. Resample on the compressed example: blockiness 2.93 → 1.46 (normal 0.97–1.06), sharpness and fine detail went down. The examples are from the training data, so their confidence is optimistic; all five L3 examples happened to be pear leaf spot.

## Photo quality check (3 Nov, computed on the 840 images)
- 16 measurements per photo (brightness, dark share, contrast, colour, grain, colour grain, sharpness, fine detail, edges, one-direction smearing, JPEG blockiness, leaf cover); random forest, tested on photos it never saw (5 groups by photo).
- Problem type right 97.7–98.0%; level right 92–94% (99.6% within one level). Grain, low light and compression always right; all mistakes are motion vs defocus blur, or mild motion blur taken for clean.
- Limit: trained on one synthetic problem per photo; a real photo with two problems (dark + compressed) got a 37%-sure wrong main problem, so the notebook builds the fix from the plain-word problem list when the forest is under 60% sure.
- Normal ranges from the 1st–99th percentiles of clean photos: 16% of clean photos get any warning, every L3 photo does (with 5th–95th: 44% of clean photos).

## Restoration test of fixes (3 Nov; SSIM to the clean photo, L3)
- Low light: gamma +0.20 (best single fix), brighten +0.15, CLAHE +0.13, CLAHE + denoise +0.22 (best).
- Grain: resample (shrink to half, enlarge back) +0.21 (best), denoise +0.12; CLAHE −0.03, sharpen −0.06.
- Compression: deblock +0.02; CLAHE −0.11, sharpen −0.09.
- Blur (motion, defocus): nothing recovers much (sharpen +0.01 on motion).
- Pixel similarity is not model accuracy: the 6 Nov L3 variants run showed most of these "restoring" fixes lower CLIP accuracy.

## Data check: PlantVillage copies (3 Nov)
- All 25 potato late blight and all 30 grape leaf blight test photos are exact PlantVillage images: never use PlantVillage photos of those two classes as references.
- None of the 30 apple scab photos (AppleLeaf9) is in PlantVillage's apple scab folder, so PlantVillage apple scab is a genuine other-source set.

## Notebooks
- SafeCrop_fairness_options.ipynb: options 1–5 (done 5 Nov). Results in SafeCrop/results/fairness.
- SafeCrop_L3_variants.ipynb: 18 versions of each L3 photo + auto (rules) and auto (learned, out-of-fold); done 6 Nov. Results in SafeCrop/results/l3_variants.
- SafeCrop_photo_check.ipynb: quality check for any photo; Nabil's version (6 Nov) uses only compression → resample. Results in SafeCrop/results/photo_check.
- SafeCrop_inference_Gemma4_31B.ipynb (4 Nov): Gemma vs plain Gemini; dropped after 180 images.

## Candidate next experiments (L3 fixed)
- Healthy pull: put noisy copies of healthy photos in the database; Gemini prompt option "can't tell, please retake" instead of guessing healthy.
- Better references at L3 (39% of L3 images have no right reference with our 7 diseases; 72% with the filled database): add noisy copies of the other photos to the database (leave-one-photo-out), or fine-tune CLIP on noisy photos. The L3 variants result points this way: fix the database side, not the photo.
- Test the photo check + resample route end to end with Gemini + references (Step 2b) on compressed L3 photos.
- Real field photos through the photo check (the forest has only seen synthetic noise).
- Option 4 for more diseases: other-source photos in SafeCrop/extra_references/<disease>/<source>/.
- Gemini prompt options still untested: crop given by the farmer (separate condition), top-3 answers with probabilities.
