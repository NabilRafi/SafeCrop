# SafeCrop: Mid-Project Report

CSE299 Junior Design, Fall 2026, Section 13, Group 7. Supervisor: Md. Salman Shamil. Submitted Week 7 (1 November 2026).
Members: Mohammad Nabil Ferdous (ID 2423275042); teammates' names and IDs to be added.

Text of the mid-project report as submitted. The figures (1-5) are in the Claude Docs version and the printed PDF; their captions are kept below.

## Summary

At mid-semester SafeCrop has a finished 840-image noisy test set, a complete three-model benchmark on all 840 images, and a working retake loop.

- **Noise cuts every model.** From clean photos (L0) to severe noise (L3), the CLIP photo database falls from 100% to 40% correct and Gemini 3.5 Flash-Lite from 67% to 13%.
- **Little-studied diseases fall further.** At L3, Gemini names 29% of info-rich photos correctly but only 2% of info-scarce ones.
- **Asking for a clearer photo wins most of it back.** Starting at L3 and retaking only when unsure, CLIP ends 88% correct after 2.6 photos on average, against 38% from one L3 photo.
- **Carrying the previous photo's features did not help.** It lowered CLIP's accuracy at every step, by up to 14 points.

Weeks 8 to 12 add the two missing Track 3 approaches (an SVM and a fine-tuned CLIP), Gemini's carried pipelines, a test on new field photos, and the live demo app.

## 1. Problem statement (updated)

SafeCrop now asks how photo quality and how well-studied a disease is change AI crop-disease diagnosis, and adds a loop that asks for a clearer photo only when the model is unsure.

**The problem.** Farmers in Bangladesh check crop diseases with phone photos that are often blurry, dark, grainy or compressed. AI diagnosis models are built and tested on clean photos. Many local diseases, such as jute mosaic, also have little research or labelled data behind them. A confident but wrong answer can lead to the wrong treatment.

**Our three questions.**

1. How much accuracy does each model lose as photo quality drops?
2. Do well-studied (info-rich) diseases hold up better under noise than little-studied (info-scarce) ones?
3. Can an agentic loop that asks for a clearer photo only when the model is unsure give reliable answers without making every user retake?

**What changed after we started, and why.**

| Part | Before | Now (Week 7) | Why it changed |
| --- | --- | --- | --- |
| Course track | Track 1: an intelligent system for a local problem | Track 3: ML model and dataset development | SafeCrop was assigned to Track 3 in Week 2 |
| Main question | Can a CLIP-based out-of-distribution gate (NegLabel + TANL) flag photos the app does not know: a new disease, a non-plant object, a blurry photo? | How much do photo noise and a disease's information richness change accuracy? | Supervisor's Week 2 advice: study two axes, image clarity and how well-studied a disease is |
| A poor photo | Rejected: "please retake the photo or consult an expert" | Answered when the model is confident; otherwise the system asks for a clearer photo | Rejecting every blurry photo is unfriendly; the supervisor asked for an agentic loop in Week 6 |
| Test data and diseases | — | Our 840-image set: 210 photos of 7 diseases at 4 noise levels; 3 info-rich and 4 info-scarce diseases, local and foreign | Noise had to be controlled level by level, and the information axis needs two clearly separated groups |
| Models | CLIP with negative labels (MCM, NegLabel, TANL) | CLIP zero-shot, CLIP photo database, Gemini 3.5 Flash-Lite; SVM and fine-tuned CLIP next | Track 3 compares a traditional method, a fine-tuned model and a zero-shot LLM API |
| Loop design | Week 6: one pipeline from L3, so each answer could be shaped by the noisier photo before it | Week 7: each level tested alone, then three pipelines (P3, P2, P1) that carry the previous level's features, at 4 angles | Supervisor's Week 7 advice: remove level-wise bias and repeat at other angles |
| Gemini model | Weeks 5–6: Gemini 3.8 Flash, 20 free requests a day | Gemini 3.5 Flash-Lite on the free AI Studio key, 500 requests a day | We do not use card-based billing; at 500 a day, Flash-Lite finished all 840 images |

## 2. What we finished so far

Six pieces are finished; the sections below show each one with its evidence and what it adds to the full project.

| Finished piece | Week | Evidence | What it adds to the full project |
| --- | --- | --- | --- |
| Disease groups from an Info-Richness Index | 4–6 | Table 1 | Defines the info-rich vs info-scarce axis the whole study compares |
| 840-image noisy test set and noise generator | 5 | Figure 1, Table 1 | The fixed test bed every model and loop is scored on |
| Three-model benchmark on all 840 images | 5–7 | Figures 2–3, Tables 2–4 | Baseline numbers and error analysis for the final comparison |
| Retake loop v1: one pipeline from L3 | 6 | Section 2.3 | First proof that asking for a clearer photo recovers accuracy |
| Retake loop v2: levels alone, three pipelines, four angles | 7 | Figures 4–5, Tables 5–6 | The agentic core of the demo app and its retake rule |
| Colab notebooks and a free-tier Gemini runner | 5–7 | Section 2.4 | Reruns every result on new photos at no cost |

### 2.1 Test set and noise generator

We built an 840-image test set: 210 public photos of 7 diseases, each also copied at three noise levels.

- **Choosing the diseases.** Our Info-Richness Index (0 to 1) averages log(1 + count) of three counts per disease: research papers (OpenAIRE), labelled public photos and words in its Wikipedia article, rescaled across 20 candidate diseases. The top of the ranking became group A (info-rich), the bottom group B (info-scarce).
- **Fair pairs.** Each info-rich disease is paired with an info-scarce one of the same symptom type and photo style: potato late blight with grape leaf blight, apple scab with pear leaf spot, rice stem borer with jute dieback.
- **Noise.** Each photo gets one of five noise types (42 photos each): sensor noise, hand-shake blur, out of focus, low light or JPEG compression. It is saved at L0 (clean), L1 (mild), L2 (medium) and L3 (severe) with a fixed seed, so the set can be rebuilt exactly.
- **Angles.** For the retake loop, every image is also rotated 90°, rotated 180° and mirrored.

**Table 1. The seven diseases in the test set**

| Disease | Group | Origin | Info-Richness Index | Photos | Photo source |
| --- | --- | --- | --- | --- | --- |
| Potato late blight | A, info-rich | Foreign | 0.98 | 25 | PlantVillage (lab photos) |
| Apple scab | A, info-rich | Foreign | 0.82 | 30 | AppleLeaf9 |
| Rice stem borer | A, info-rich | Local | 0.72 | 30 | Mendeley, Bangladeshi field photos |
| Pear leaf spot | B, info-scarce | Foreign | 0.39 | 35 | DiaMOS Plant |
| Grape leaf blight | B, info-scarce | Foreign | 0.38 | 30 | PlantVillage (lab photos) |
| Jute mosaic | B, info-scarce | Local | 0.19 | 30 | Harvard Dataverse, Bangladeshi field photos |
| Jute dieback | B, info-scarce | Local | 0.08 | 30 | Harvard Dataverse, Bangladeshi field photos |

Total: 85 info-rich and 125 info-scarce photos, 210 × 4 levels = 840 images. Black gram yellow mosaic (local, info-rich, index 0.65) is in our design but has no photos yet.

*Figure 1. One apple scab photo at the four noise levels (columns, L3 to L0) and the four angles (rows), as produced by our notebooks.*

**What it adds to the full project:** every result in this report is measured on these same 840 images, so models and loops are compared fairly. The noise levels and angles are the "new or changed data" test that Track 3 asks for.

**Limits:** the noise is synthetic, and potato and grape photos come from a lab set (PlantVillage), so a model can partly match photo style instead of the disease.

### 2.2 Three-model benchmark on all 840 images

Every model loses most of its accuracy as noise grows, and the CLIP photo database is the most accurate at every level.

- **CLIP zero-shot** (ViT-L/14): picks the closest of 33 text labels (our diseases, same-crop look-alikes and "healthy" for each crop). No training.
- **CLIP photo database:** the 5 most similar clean photos of other plants vote, never the photo's own clean copy. Chooses among the 7 diseases.
- **Gemini 3.5 Flash-Lite** (free API): gets the same 33 labels and returns a diagnosis, a confidence and a "clear enough" flag as JSON.

*Figure 2. Share of the 210 images at each noise level where the model named the right disease.*

Info-scarce diseases lose more. At L3 the database names 48% of info-rich photos correctly against 34% of info-scarce ones; Gemini manages 29% against 2%. Zero-shot is weak everywhere, and its clean-photo score comes mostly from two foreign info-scarce diseases (pear 71%, grape 63%).

*Figure 3. The same accuracy split into info-rich (group A, 85 photos) and info-scarce (group B, 125 photos) diseases.*

**Table 2. Correct disease by disease: clean (L0) vs noisy (L1–L3)**

| Disease (group) | Zero-shot clean | Zero-shot noisy | Database clean | Database noisy | Gemini clean | Gemini noisy |
| --- | --- | --- | --- | --- | --- | --- |
| Potato late blight (A) | 40% | 15% | 100% | 77% | 92% | 59% |
| Apple scab (A) | 0% | 11% | 100% | 48% | 43% | 21% |
| Rice stem borer (A) | 0% | 0% | 100% | 100% | 87% | 68% |
| Pear leaf spot (B) | 71% | 16% | 100% | 70% | 89% | 20% |
| Grape leaf blight (B) | 63% | 16% | 100% | 94% | 67% | 20% |
| Jute mosaic (B) | 0% | 2% | 100% | 58% | 17% | 2% |
| Jute dieback (B) | 0% | 4% | 100% | 33% | 73% | 21% |

Clean = 25–35 photos per disease; noisy = 75–105 images. Gemini called clean jute mosaic "jute anthracnose" in 24 of 30 photos.

**Table 3. What kind of mistakes each model makes (% of all 840 answers)**

| Model | Correct | Wrong crop | Right crop, wrong disease | Said "healthy" |
| --- | --- | --- | --- | --- |
| CLIP zero-shot | 13% | 47% | 28% | 12% |
| CLIP photo database | 76% | 22% | 1% | 0% |
| Gemini 3.5 Flash-Lite | 39% | 28% | 27% | 7% |

Wrong crop is the largest error for all three models. At L3, Gemini's most common answer was "Apple: healthy" (61 of 210 images). By noise type (L1–L3), JPEG compression hurt least (database 78% correct, Gemini 40%); out-of-focus blur and sensor noise hurt the database most (62%, 61%), and low light hurt Gemini most (19%).

**Table 4. Gemini's own "clear enough" flag**

| Level | Asked for a retake (of 210) | Correct when it said "clear enough" | Correct when it asked for a retake |
| --- | --- | --- | --- |
| L0 clean | 1 | 67% | 0 of 1 |
| L1 mild | 34 | 52% | 32% |
| L2 medium | 134 | 42% | 17% |
| L3 severe | 171 | 28% | 9% |

Gemini's retake request is a useful signal: answers on photos it calls clear are right 1.6 to 3 times as often. Its single answers also vary: asked the same 840 images again in the loop notebook, it gave the same answer 63% of the time (80% at L0, 52% at L3), with the same overall accuracy, 38.6%.

**What it adds to the full project:** these are the baseline numbers the final report compares the SVM and the fine-tuned CLIP against. They show where each model fails (wrong crop, local jute diseases, severe noise) and why one look at a poor photo is not enough, which is the reason for the retake loop.

**Limits:** the database's 100% on clean photos is inflated, because each disease comes from one photo source and the model can match photo style. Chance alone can move a level's accuracy by about ±7 points, and a single disease's by up to ±18 (95% margins).

### 2.3 Agentic retake loop

Asking for a clearer photo only when the model is unsure brings accuracy back: starting from severe noise, CLIP ends 88% correct after 2.6 photos on average.

*Figure 4. The retake loop. "Confident" means: for CLIP, our quality score is at least 0.8 (a logistic regression on 8 photo-quality features plus CLIP's own confidence); for Gemini, it says "clear enough" with confidence of at least 0.8.*

**v1 (Week 6).** One pipeline from L3 with the CLIP photo database on 210 photos: 40.0% correct from the L3 photo alone, 88.6% after the loop, using 2.40 photos on average. Stopping on CLIP's own confidence instead was confidently wrong on 31.9% of photos; our quality score cut that to 11.4%.

**v2 (Week 7), after the supervisor's review.** Each level is first tested on its own, with nothing carried over (Table 5). Three pipelines then start at L3 (P3), L2 (P2) or L1 (P1) and carry the previous level's features: CLIP mixes the two image embeddings half and half, and Gemini gets its own notes on the previous photo. CLIP ran at all four angles (3,360 single tests, 2,520 pipeline runs); Gemini ran at the original angle to fit the free quota (840 single tests).

**Table 5. Each level judged on its own (% of tests)**

| Model | Measure | L0 clean | L1 mild | L2 medium | L3 severe |
| --- | --- | --- | --- | --- | --- |
| CLIP database, 840 tests per level | Correct | 99.9% | 90.8% | 68.5% | 38.5% |
|  | Confident | 99.2% | 77.4% | 44.8% | 20.5% |
|  | Confident but wrong | 0.0% | 1.5% | 3.5% | 4.4% |
| Gemini 3.5 Flash-Lite, 210 tests per level | Correct | 61.4% | 51.4% | 26.7% | 14.8% |
|  | Confident | 98.1% | 72.4% | 28.1% | 17.6% |
|  | Confident but wrong | 36.7% | 27.6% | 13.8% | 10.0% |

Gemini is confident but wrong on 37% of clean photos, so its own confidence cannot be the only stop rule. (Its numbers differ slightly from Section 2.2 because it was asked again.)

*Figure 5. Accuracy of the start level judged alone and after the retake loop, with the average number of photos used. CLIP: 840 runs per pipeline. Gemini: 210 runs per pipeline, worked out from its single-level answers with nothing carried.*

The loop more than triples Gemini's L3 accuracy (15% to 51%) but stays far below CLIP, because Gemini often stops on a confident wrong answer (48% of P3 runs).

**Table 6. Carrying the previous level's features lowered CLIP's accuracy at every step**

| Pipeline step | Images | With features carried | Same images judged alone | Change |
| --- | --- | --- | --- | --- |
| P3: L3 to L2 | 668 | 48.7% | 62.7% | −14.0 pts |
| P3: L2 to L1 | 467 | 80.1% | 87.6% | −7.5 pts |
| P3: L1 to L0 | 198 | 99.0% | 99.5% | −0.5 pts |
| P2: L2 to L1 | 464 | 76.9% | 86.0% | −9.1 pts |
| P2: L1 to L0 | 225 | 98.2% | 99.6% | −1.4 pts |
| P1: L1 to L0 | 190 | 98.4% | 99.5% | −1.1 pts |

Carrying makes CLIP hold on to its earlier, often wrong answer: at P3's first carried step it kept the previous answer 72% of the time, against 53% when the two levels were judged separately. Rotating or mirroring the photo changed CLIP's accuracy by at most 7.6 points (L2: 64.3% at 90° vs 71.9% original), and on clean photos 99.5% got the same answer at all four angles. Info-scarce photos needed more photos in every pipeline (P3: CLIP 2.79 vs 2.28, Gemini 2.96 vs 2.54).

**What it adds to the full project:** the loop is the agentic core of the live demo, deciding when to ask the farmer for a clearer photo. Its photos-versus-accuracy numbers set the demo's stop rule, and Table 6 tells us to judge each new photo on its own rather than mix in the earlier, noisier one.

**Limits:** the "clearer photos" are our own noise levels, not real retakes, and the angles are rotations of the same photo, not new shots.

### 2.4 Notebooks and tools

Four Google Colab notebooks rebuild every number in this report from the raw photos, at no cost.

| Notebook | What it does | Main outputs |
| --- | --- | --- |
| Noise generator | Makes the L1–L3 copies of every photo with a fixed seed; reads nested photo folders | The 840-image test set |
| Inference (CLIP zero-shot, CLIP database, Gemini) | Runs the three models on the same images; Gemini answers are cached and resume after a stop | results_tables.xlsx and 5 figures |
| Retake loop v1 | One pipeline from L3 with the quality-score stop rule | Week 6 tables and figures |
| Retake loop v2 | Levels alone, pipelines P3/P2/P1, carry effect, four angles | loop_v2_results.xlsx and 3 charts |

- **Free-tier runner.** Gemini is paced at 14 requests a minute (the limit is 15) and backs off after a rate-limit error. When the 500-a-day limit is reached, the run continues the next day from its cache.
- **Fair partial results.** Gemini works through the photos in a fixed random order, and the tables only use photos it has finished, so a half-done run is not biased toward easy photos.
- **No lost answers.** If Gemini's reply breaks the JSON format, the parser falls back to plain JSON and then to plain text.
- **CLIP quality score.** A logistic regression on 8 photo-quality features plus CLIP's confidence, trained out-of-fold so a photo is never scored by a model that saw it.

**What it adds to the full project:** new photos (field photos, black gram) go through the same notebooks unchanged, so the final results stay comparable. This is also the code we will present from GitHub.

## 3. What is left, week by week

Five class weeks remain; the course timeline puts the final presentation, live demo and final report in Weeks 11 and 12.

| Week | Class | Work | Output |
| --- | --- | --- | --- |
| 8 | 8 Nov | Finish Gemini's carried pipelines: 42 of 210 photos are done, and on those, carrying lowered P3 from 66.7% to 50.0% correct. Run Gemini's "memory" loop, where one chat sees each clearer photo. Train an SVM on CLIP features as the traditional-ML baseline. | Loop v2 tables complete for both models; SVM accuracy at L0–L3 |
| 9 | 15 Nov | Fine-tune CLIP on clean and noisy copies, splitting train and test by photo so no photo appears in both. Compare all approaches on the same 840 images, with error analysis per disease and noise type. | Fine-tuned model results; four-way comparison |
| 10 | 22 Nov | Test on new real field photos of local diseases, including black gram yellow mosaic. Write the labelling guidelines and a data card (sources, licences, limits). Build the demo's back end (FastAPI) around the retake loop. | New-data results, data card, working API |
| 11 | 29 Nov | Build the demo front end (React): upload a photo, get a diagnosis or a request for a clearer one. Measure response time and cost per diagnosis. Record the one-minute demo video and finish the GitHub README. Final presentations and live demos begin. | Demo app, video, slides |
| 12 | 6 Dec | Final presentation and live demo; submit the final report (8 pages) as a PDF and a printed copy. | Final report |

Class dates follow the Sunday classes of Weeks 2–7. Weekly progress updates continue through Week 10.

## 4. Features we are aiming for in the final report

The final report will present a working retake system and a four-way comparison of approaches on noisy and new photos.

| Feature in the final report | Status at Week 7 |
| --- | --- |
| Four approaches on the same 840 images: an SVM on CLIP features (traditional ML), fine-tuned CLIP, the CLIP photo database and Gemini 3.5 Flash-Lite (zero-shot LLM API), with CLIP zero-shot as the floor | Database, Gemini and zero-shot done; SVM and fine-tuned CLIP in Weeks 8–9 |
| Accuracy against noise for every approach, split into info-rich vs info-scarce and local vs foreign diseases | Done for three approaches |
| The retake loop for both models: photos used, accuracy and "confident but wrong" per pipeline and angle | CLIP done; Gemini's carried runs at 42 of 210 photos |
| Tests on new or changed data: noise levels, four angles and new real field photos | Noise and angles done; field photos in Week 10 |
| Error analysis: wrong crop vs wrong disease, per disease and per noise type | Done for three approaches |
| Live demo app: upload a photo, get a diagnosis or a request for a clearer photo, with response time and cost per diagnosis | Weeks 10–11 |
| Dataset description: labelling guidelines, sources and licences, known limits | Sources and licences recorded; guidelines in Week 10 |
| An honest failure report: synthetic noise, one photo source per disease, Gemini's 63% run-to-run agreement | Collected as we go |

## Links and references

**Project links**

- Inference notebook (Colab): [colab.research.google.com/drive/1MGAM3DckhtF0a08q17UCe_D_JG8p0q4H](https://colab.research.google.com/drive/1MGAM3DckhtF0a08q17UCe_D_JG8p0q4H)
- Retake loop v2 notebook (Colab): [colab.research.google.com/drive/1eFHy3ro_0QiGb2fVCTGxtHoLnJrnUGMc](https://colab.research.google.com/drive/1eFHy3ro_0QiGb2fVCTGxtHoLnJrnUGMc)
- Dataset (Google Drive): [drive.google.com/drive/folders/1q3rB5OeE9UBq9kQnvbbMCx996hbczyhh](https://drive.google.com/drive/folders/1q3rB5OeE9UBq9kQnvbbMCx996hbczyhh?usp=sharing)
- Weekly update slides, Weeks 2–7: [docs.google.com/presentation/d/1KkVdkICk_VG6YZ4rQ4t9wxhNECiaVwDXkRA84GV755U](https://docs.google.com/presentation/d/1KkVdkICk_VG6YZ4rQ4t9wxhNECiaVwDXkRA84GV755U/edit)

**References**

1. A. Radford et al., "Learning Transferable Visual Models From Natural Language Supervision" (CLIP), ICML 2021. [arXiv:2103.00020](https://arxiv.org/abs/2103.00020)
2. Y. Ming et al., "Delving into Out-of-Distribution Detection with Vision-Language Representations" (MCM), NeurIPS 2022.
3. X. Jiang et al., "Negative Label Guided OOD Detection with Pretrained Vision-Language Models" (NegLabel), ICLR 2024. [arXiv:2403.20078](https://arxiv.org/abs/2403.20078)
4. TANL, "Activation Matters", CVPR 2026. [arXiv:2603.25250](https://arxiv.org/abs/2603.25250)
5. D. P. Hughes and M. Salathé, "An open access repository of images on plant health to enable the development of mobile disease diagnostics" (PlantVillage), 2015. [arXiv:1511.08060](https://arxiv.org/abs/1511.08060)
6. AppleLeaf9 apple leaf disease dataset (apple scab photos), CC BY 4.0.
7. DiaMOS Plant dataset (pear leaf spot photos), CC BY 4.0.
8. Rice stem borer damage photos (dead heart, white head), Mendeley Data, dataset hnfjs42d5g, CC BY 4.0.
9. Jute disease photos (mosaic, dieback), Harvard Dataverse, [doi:10.7910/DVN/FJ1DM1](https://doi.org/10.7910/DVN/FJ1DM1), CC0.
10. OpenAIRE Graph: publication counts used in the Info-Richness Index.
11. Google, Gemini 3.5 Flash-Lite, used through the free Google AI Studio API, October 2026.

AI tools: Claude (Anthropic) helped write the notebook code and draft this report.
