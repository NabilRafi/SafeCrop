# SafeCrop disease groups (decided 9 Oct 2026, pending supervisor OK)

Full evidence (chart, 20-candidate counts, image sources, search strings): "Disease groups" tab of the SafeCrop — Week 4 Plan doc, https://claude.ai/code/artifact/1155f5e9-bfe1-458f-8a7c-89fb8ac22ccf

## Groups (Info-Richness Index in brackets)
- Group A, info-rich: Western = potato late blight (0.98), apple scab (0.82). Local = rice stem borer damage (0.72), black gram yellow mosaic (0.65).
- Group B, info-scarce: Western = pear leaf spot (0.39), grape leaf blight / Isariopsis leaf spot (0.38). Local = jute mosaic (0.19), jute dieback (0.08).
- Team suggestions: potato late blight, rice stem borer and jute mosaic are in. Brown planthopper is out for now (index 0.57; only 71 public damage photos, no licence).

## Matched pairs (same symptom type, same photo style)
- W1 blight: potato late blight vs grape leaf blight (PlantVillage, lab).
- W2 leaf spots: apple scab vs pear leaf spot (AppleLeaf9 vs DiaMOS Plant, orchard field photos).
- L1 shoot dieback: rice stem borer (dead heart, white head) vs jute dieback (Bangladeshi field photos).
- L2 yellow mosaic (begomovirus): black gram yellow mosaic vs jute mosaic (Bangladeshi field photos).

## Checks
- Gap within origin: Western 0.43, local 0.46 (rule: at least 0.3). Pooled gap 0.27 with no overlap; rice tungro (0.71) instead of black gram would give 0.32 but breaks the symptom match.
- Every A beats every B on all three counts; separation holds when any one count is dropped.

## Index method
Papers = OpenAIRE Graph publications matching "disease name" AND crop (OpenAlex was blocked for automated search; Member 2 to re-check by hand). Images = original labelled public images (damage photos for pests). Web = prose words of the English Wikipedia article on the disease or its cause (XTools). Index = mean of log(1 + count) rescaled 0–1 across 20 candidates.

## Image sources for the eight
PlantVillage (potato late blight 1,000; grape leaf blight 1,076; CC BY-SA 3.0) · AppleLeaf9 Scab (5,410; CC BY 4.0) · DiaMOS Plant leaf "spot" (884; CC BY 4.0; 13.1 GB zip) · Mendeley hnfjs42d5g stem borer (dead heart 439, white head 551; CC BY 4.0) · Harvard Dataverse jute set doi:10.7910/DVN/FJ1DM1 (mosaic 240, dieback 300; CC0) · Mendeley z55yrbmn2d IDBGL black gram yellow mosaic (1,681; CC BY 4.0).

Workload: 8 diseases × 20 = 160 clean images, 480 blurred copies, 960 "recognizable?" labels (two annotators).
