# E0: frozen CLIP baseline

Run folder: `results/baseline/20261111-152201_clip-vit-large-patch14_e0_8d`

- model openai/clip-vit-large-patch14, k = 5, leave-one-photo-out, 8 diseases
- CLIP database, frozen clip-vit-large-patch14 (recomputed): 838/840 predictions identical to the saved Step 2 file clip_database_7.csv (black gram is an extra choice here)
- CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed): 833/840 predictions identical to the saved Step 2 file clip_zero_shot_33.csv (black gram is an extra choice here)
- 8 DISEASES: black gram yellow mosaic is an 8th choice (30 photos, 120 images, its own folds). The 840 original images come first so they stay comparable (these methods could also answer black gram, an 8th option the earlier 7-disease runs did not have).

## The original images (7 diseases): comparable with every earlier number

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 100.0 | 93.3 | 71.9 | 40.0 | 76.3 | 840 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 25.7 | 15.2 | 8.6 | 3.8 | 13.3 | 840 |
| CLIP database, frozen (Step 2) | 100.0 | 93.3 | 71.9 | 40.0 | 76.3 | 840 |
| Gemini + references + descriptions (Step 2b) | 100.0 | 92.9 | 75.2 | 47.1 | 78.8 | 840 |
| Gemini plain, 33 options (Step 2) | 66.7 | 48.6 | 26.2 | 12.9 | 38.6 | 840 |
| CLIP zero-shot, 33 options (Step 2) | 25.7 | 15.2 | 8.6 | 3.8 | 13.3 | 840 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 81.2 | 48.2 | 73.0 | 34.4 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 9.1 | 3.5 | 16.2 | 4.0 |
| CLIP database, frozen (Step 2) | 81.2 | 48.2 | 73.0 | 34.4 |
| Gemini + references + descriptions (Step 2b) | 80.6 | 48.2 | 77.6 | 46.4 |
| Gemini plain, 33 options (Step 2) | 54.7 | 29.4 | 27.6 | 1.6 |
| CLIP zero-shot, 33 options (Step 2) | 9.1 | 3.5 | 16.2 | 4.0 |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 26.2 | 33.3 | 28.6 | 54.8 | 57.1 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 4.8 | 0.0 | 0.0 | 11.9 | 2.4 |
| CLIP database, frozen (Step 2) | 26.2 | 33.3 | 28.6 | 54.8 | 57.1 |
| Gemini + references + descriptions (Step 2b) | 31.0 | 52.4 | 38.1 | 52.4 | 61.9 |
| Gemini plain, 33 options (Step 2) | 9.5 | 14.3 | 14.3 | 4.8 | 21.4 |
| CLIP zero-shot, 33 options (Step 2) | 4.8 | 0.0 | 0.0 | 11.9 | 2.4 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 61.1 | 70.6 | 61.9 | 70.6 | 77.8 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 5.6 | 9.5 | 7.1 | 16.7 | 7.1 |
| CLIP database, frozen (Step 2) | 61.1 | 70.6 | 61.9 | 70.6 | 77.8 |
| Gemini + references + descriptions (Step 2b) | 61.1 | 78.6 | 65.9 | 69.0 | 84.1 |
| Gemini plain, 33 options (Step 2) | 25.4 | 34.9 | 26.2 | 19.0 | 40.5 |
| CLIP zero-shot, 33 options (Step 2) | 5.6 | 9.5 | 7.1 | 16.7 | 7.1 |

### Head to head (McNemar exact test)

| New | Baseline | Levels | Images | Only new right | Only baseline right | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | CLIP database, frozen (Step 2) | All | 840 | 0 | 0 | 1.000 |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | CLIP database, frozen (Step 2) | L3 | 210 | 0 | 0 | 1.000 |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | Gemini + references + descriptions (Step 2b) | All | 840 | 12 | 33 | 0.002 |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | Gemini + references + descriptions (Step 2b) | L3 | 210 | 3 | 18 | 0.001 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | CLIP database, frozen (Step 2) | All | 840 | 15 | 544 | <0.001 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | CLIP database, frozen (Step 2) | L3 | 210 | 7 | 83 | <0.001 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | Gemini + references + descriptions (Step 2b) | All | 840 | 17 | 567 | <0.001 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | Gemini + references + descriptions (Step 2b) | L3 | 210 | 7 | 98 | <0.001 |

## Black gram yellow mosaic only (no earlier baselines)

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 100.0 | 66.7 | 20.0 | 6.7 | 48.3 | 120 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 0.0 | 3.3 | 6.7 | 10.0 | 5.0 | 120 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 48.3 | 6.7 | nan | nan |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 5.0 | 10.0 | nan | nan |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 0.0 | 0.0 | 0.0 | 0.0 | 33.3 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 16.7 | 0.0 | 0.0 | 0.0 | 33.3 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 27.8 | 22.2 | 27.8 | 0.0 | 77.8 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 16.7 | 0.0 | 5.6 | 0.0 | 11.1 |

## All images (8 diseases)

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 100.0 | 90.0 | 65.4 | 35.8 | 72.8 | 960 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 22.5 | 13.8 | 8.3 | 4.6 | 12.3 | 960 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 72.6 | 37.4 | 73.0 | 34.4 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 8.0 | 5.2 | 16.2 | 4.0 |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 22.9 | 29.2 | 25.0 | 47.9 | 54.2 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 6.2 | 0.0 | 0.0 | 10.4 | 6.2 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 56.9 | 64.6 | 57.6 | 61.8 | 77.8 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [8 diseases] | 6.9 | 8.3 | 6.9 | 14.6 | 7.6 |

### Correct neighbours among the k database photos

| Level | Images | No correct neighbour | At least 1 correct (%) | Mean correct of k |
| --- | ---: | ---: | ---: | ---: |
| L0 | 240 | 0 | 100.0 | 4.9 |
| L1 | 240 | 9 | 96.2 | 4.2 |
| L2 | 240 | 46 | 80.8 | 3.0 |
| L3 | 240 | 104 | 56.7 | 1.8 |
| All | 960 | 159 | 83.4 | 3.5 |
