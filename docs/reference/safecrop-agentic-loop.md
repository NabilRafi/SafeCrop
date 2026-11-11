# SafeCrop: agentic loop and Gemini (Weeks 6–7, updated 30 Oct 2026)

## Week 7 (30 Oct 2026): loop v2 — levels alone, three pipelines, angles

### Supervisor's instruction (after the Week 6 update)
- **Remove level-wise bias.** In last week's loop, the answer at L2 could be shaped by what was seen at L3.
- **Run every image at every level on its own**, with no features from any other level. This gives a clean accuracy per level.
- **Keep the pipeline idea, as three pipelines.** Each moves to the next level only if the model isn't confident, and carries features from the immediately previous level:
  - P3: L3 → L2 → L1 → L0
  - P2: L2 → L1 → L0
  - P1: L1 → L0
- **Repeat everything at different angles/sides**, for both the levels-alone tests and the pipelines.

### Model decision (30 Oct)
- Nabil won't use any card, so there is no Google Cloud billing.
- Everything runs on the **free AI Studio key**.
- Free-key limits seen in AI Studio:
  - Gemini 3.8 Flash: 5 RPM, 20 RPD.
  - Gemini 3.5 Flash-Lite: 15 RPM, 500 RPD.
  - Gemma 4 26B/31B: 30 RPM, 14.4K RPD.
- **Chosen: CLIP + Gemini 3.5 Flash-Lite only.** No Gemma, no 3.8 Flash.
- Published tests put Flash-Lite behind 3.8 Flash on vision:
  - Roboflow identification: 84% vs 98%.
  - MMMU Pro: 84% vs 89%.

### Design choices (to confirm with the supervisor)
- **Angles are synthetic views of the same photo.** Default: original, rot90, rot180, mirror. Optional: rot45 (corners filled by reflection), rot270, tilt (perspective). They aren't new photos; mirror stands in for "the other side".
- **CLIP runs all 4 angles.** Gemini runs the original angle only (`GEMINI_VIEWS`), to fit the free quota.
- **Every pipeline continues to L0 if needed.** Stop rules are unchanged:
  - Gemini: clear_enough and confidence ≥ 0.8.
  - CLIP: qc ≥ 0.8.
- **Only the immediately previous level is carried.**
  - CLIP: query = normalize(0.5·current + 0.5·previous image embedding).
  - Gemini: its own notes from the previous step (visible_signs ≤ 25 words, diagnosis, confidence). The "notes+photo" option also sends the previous photo.
- **A pipeline's first step is the level-alone answer.**
- **Gemini order:**
  - Part 1 asks every image on its own (840 questions); Part 2 runs the pipelines.
  - Photos follow a fixed random order per angle (seed 299+2+angle index).
  - Pipelines are reported only for pairs Part 2 has reached, in that order (`finished_pairs`). Otherwise the partial tables would show only the photos that were confident at the first try.

### Notebooks
- **SafeCrop_loop_v2_three_pipelines.ipynb**
  - Results go to SafeCrop/results/loop_v2. Output files are prefixed with the model name.
  - Tables:
    1. Levels alone
    2. Pipelines, including "nothing carried" = last week's loop on the same photos
    3. Carry effect
    4. Angles
    5. Groups A/B
- **SafeCrop_inference_CLIP_GeminiFlashLite.ipynb**
  - Three-way comparison: CLIP zero-shot vs CLIP photo database vs Gemini 3.5 Flash-Lite.
  - Answers go to their own file, gemini_3.5_flash_lite_predictions.csv. Last week's 3.8 Flash answers are never mixed in.
  - It reuses the loop's alone/original answers when both notebooks share the same Drive results folder.
- **Folder issue on 30 Oct:** the inference zip had no loop_v2 folder, and both notebooks asked Gemini separately (490 + 497 answers). So they saved to different places, probably a different Google account or Drive not mounted.
  - Advice given: check that My Drive/SafeCrop/results/loop_v2 exists. If not, create it and upload gemini_v2_calls.csv from the loop zip.
  - Run both notebooks from one account, loop notebook first.

### First real results — loop notebook (30 Oct, 20:54–21:30 Dhaka)
- **CLIP: complete.** 210 photos × 4 levels × 4 angles = 3,360 tests, plus 2,520 pipeline runs.
  - Levels alone: L3 38.4%, L2 68.4%, L1 90.8%, L0 99.9%.
  - The original angle matches last week exactly: 40.0 / 71.9 / 93.3 / 100, and all 840 predictions are identical.
  - Confident: L3 20.5%, L2 44.8%, L1 77.4%, L0 99.2%. Confident but wrong is 4.4% at most.
  - Pipelines with features carried:
    - P3: 2.59 tries, 87.7% right. Nothing carried: 2.52 tries, 91.0%.
    - P2: 1.82 tries, 94.5%. Nothing carried: 1.75 tries, 95.0%.
    - P1: 1.23 tries, 98.1%. Nothing carried: 98.3%.
  - P3 confident but wrong: 12.1% with features carried vs 8.9% with nothing carried.
  - **Carrying never helped CLIP**:
    - P3 L3→L2: −14.1 points (48.7% vs 62.7% on the same images).
    - P2 L2→L1: −9.1. P3 L2→L1: −7.5. Steps into L0: about −1.
  - **Anchoring at the first carried step**: CLIP kept its previous answer 72% vs 53% when the two levels were judged alone (P2: 66% vs 55%).
  - **Angles**: rot90 is worst (L2 64.3% vs 71.9% original; P3 83.8% vs 87.6%). Same answer at all 4 angles: 73% at L2 and L3, 99.5% at L0.
  - **Groups**: A vs B at L3 is 45% vs 34%; at L0, 100% vs 99.8%. P3 tries 2.3 vs 2.8.
- **Gemini 3.5 Flash-Lite: 490 of 840 images answered.**
  - 121 photos have all 4 levels, 4 are partial, 85 not started.
  - Part 2 not started; about 600 carry questions estimated.
  - Levels alone: L3 16.0%, L2 26.0%, L1 55.4%, L0 62.8%.
  - Confident: 18.4 / 32.5 / 71.9 / 96.7%. Confident but wrong: 9.6 / 14.6 / 24.8 / 33.9%.
  - Nothing-carried loop:
    - P3: 2.75 tries, 53.3% right, 45% confident but wrong.
    - P2: 1.93 tries, 57.4%.
    - P1: 1.28 tries, 61.2%.
  - **Groups**: A vs B is L3 38.8% vs 1.3%, L2 51.1 vs 10.5, L1 80.4 vs 40.0, L0 78.3 vs 53.3. Nothing-carried P3: A 2.35 tries / 76.1%, B 2.99 tries / 39.5%.
  - **Typical mistakes**: at L3, 69 of 125 answers were "Apple: healthy". At L0, jute mosaic was called "Jute: anthracnose" 16 of 18 times.
  - **Same 30 images as last week's 3.8 Flash**: 3.8 Flash got 20 right, Flash-Lite 18.
- **Explainer PDF**: SafeCrop_loop_results_explained_30Oct2026.pdf.
- **Caveat**: the first notebook output showed Gemini pipeline rows with 1.0 tries (23/40/87 runs). Those were partial and biased. Fixed in the updated notebook.

### First real results — inference notebook (30 Oct, 21:27–22:06 Dhaka)
- **Coverage**: CLIP on all 840 images (same as last week). Gemini 3.5 Flash-Lite on 497 images: 125 photos (124 with all 4 levels, plus 1 L0); 343 left.
- **Accuracy on the same 497 images** (L0 / L1 / L2 / L3, all levels):
  - CLIP zero-shot: 29 / 19 / 6 / 3, all 14%.
  - CLIP photo database: 100 / 93 / 71 / 40, all 76%.
  - Gemini Flash-Lite: 68 / 50 / 26 / 15, all 40%.
- **Info-rich vs info-scarce** (all levels):
  - Gemini: A 57% vs B 26%. At L3: 33% vs 0%. At L2: 51% vs 6%.
  - CLIP database: 82% vs 71%.
  - CLIP zero-shot: reversed, 10% vs 18%. It gets grape (81%) and pear (76%) clean right but 0% on apple scab, rice and jute.
- **By disease** (Gemini clean / noisy): potato 94/63, rice 82/67, jute mosaic 12/0 (called anthracnose 14 of 17 times).
- **Noise type** (noisy images):
  - Database: out of focus 57%, sensor noise 62%, compression 71%, low light 77%, hand-shake blur 74%.
  - Gemini: 26–36% for every kind.
- **Local vs foreign**: zero-shot gets 0% on local (rice, jute) clean photos. Gemini: local 39% vs foreign 40% overall.
- **Crop right**: Gemini 100% on clean photos.
- **Error types**:
  - Gemini: 40% correct, 26% wrong disease/right crop, 6% said healthy, 28% wrong crop.
  - Database: 76% correct, 22% wrong crop.
- **Gemini retake flag**: says "clear enough" for 100% of L0 and 19% of L3 images. Accuracy when clear: 68 / 52 / 35 / 21% (L0–L3).
- **Run-to-run consistency**: on 292 images answered in both notebooks, Flash-Lite gave the same answer 68% of the time (43% right both times). The two notebooks together cover 695 of 840 images.
- **Explainer PDF**: SafeCrop_inference_results_explained_30Oct2026.pdf.

## Week 6 (25 Oct 2026)

On 25 Oct the supervisor asked for three things: explain the info-rich/scarce split, build an agentic loop, and get around the Gemini API limits.
Explanation doc: https://claude.ai/artifact/K7wSSvWgCHGhmTvKG6mLZN
Deliverables made on 24–25 Oct:
- SafeCrop_agentic_loop.ipynb (Colab)
- SafeCrop_weekly_update_25Oct2026.pdf (one page)
- SafeCrop_week6_what_we_did_explained.pdf (plain-language talk track, 8 pages)

### Loop design (v1)
- **"forget" (main):** start each photo at L3. Each model answer = 1 try. If the model isn't confident, show the same photo one level clearer (L3 -> L2 -> L1 -> L0) and stop at the first confident answer. If it is still not confident at L0, record "never confident". So each photo takes 1–4 tries.
- **"remember" (optional):** each clearer photo is added to the same Gemini conversation.
- **Stop rules:**
  - Gemini: clear_enough == True and confidence >= 0.8.
  - CLIP: measured score qc >= 0.8, where qc = out-of-fold logistic regression on 8 quality features + CLIP confidence. Folds: fold = (n_groups - 1 - g) mod 5 over factorized photo_id.

### Week 6 results
CLIP photo database, 210 photos (replay):

| Stop rule | Tries | Final accuracy | Confident but wrong |
|---|---|---|---|
| No loop (L3 only) | 1 | 40.0% | - |
| Own confidence >= 0.8 | 1.70 | 68.1% | 31.9% |
| qc >= 0.8 | 2.40 | 88.6% | 11.4% |

- With qc >= 0.8:
  - Group A needs 2.02 tries and group B needs 2.66.
  - Accuracy is 86% (A) and 90% (B).
- qc threshold sweep (tries / accuracy):
  - 0.6: 2.00 / 78.6%
  - 0.7: 2.18 / 84.8%
  - 0.8: 2.40 / 88.6%
  - 0.9: 2.93 / 97.1%
  - 0.95: 3.34 / 99.5%
- **Gemini 3.8 Flash first look** (9 complete photos from 38 answers): 2.89 tries, 8/9 right vs 5/9 from one look at L3. Proof of concept only.
- Per level, those answers were confident at: L0 100%, L1 60%, L2 33%, L3 22%.

## Gemini API limits and Google Cloud (background)
- **AI Studio free tier:** per-model daily limits (see "Model decision" above). No card needed. Daily limits reset at midnight US Pacific: 1 pm Dhaka, 2 pm from 2 Nov.
- **Google Cloud free trial:** $300 for 90 days. It needs a card for verification. Not used, because Nabil won't use a card.
- **Naming:** Vertex AI is now "Gemini Enterprise Agent Platform". The API is the "Agent Platform API" (aiplatform.googleapis.com). The role is "Agent Platform User".
