# E0: frozen CLIP baseline

Run folder: `results/baseline/20261111-152229_clip-vit-large-patch14_e0_8d_rb`

- model openai/clip-vit-large-patch14, k = 5, leave-one-photo-out, 8 diseases
- TEST SET: recipe B = the same photos, noise types and folds, with L1-L3 made by a different noise recipe (src/safecrop/noise_b.py). The Step 2 / 2b baselines were scored on the original images, so they are not shown or tested here.
- 8 DISEASES: black gram yellow mosaic is an 8th choice (30 photos, 120 images, its own folds). The 840 original images come first so they stay comparable (these methods could also answer black gram, an 8th option the earlier 7-disease runs did not have).

## The original images (7 diseases): comparable with every earlier number

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 100.0 | 85.2 | 55.7 | 30.5 | 67.9 | 840 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 25.7 | 14.3 | 10.5 | 1.4 | 13.0 | 840 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 74.1 | 41.2 | 63.6 | 23.2 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 6.2 | 1.2 | 17.6 | 1.6 |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 14.3 | 28.6 | 21.4 | 28.6 | 59.5 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 0.0 | 0.0 | 0.0 | 4.8 | 2.4 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 50.8 | 53.2 | 50.8 | 50.0 | 81.0 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 7.9 | 4.8 | 7.9 | 7.1 | 15.9 |


## Black gram yellow mosaic only (no earlier baselines)

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 100.0 | 46.7 | 23.3 | 0.0 | 42.5 | 120 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 0.0 | 3.3 | 13.3 | 13.3 | 7.5 | 120 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 42.5 | 0.0 | nan | nan |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 7.5 | 13.3 | nan | nan |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 16.7 | 0.0 | 16.7 | 33.3 | 0.0 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 11.1 | 22.2 | 16.7 | 0.0 | 66.7 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 16.7 | 0.0 | 22.2 | 11.1 | 0.0 |

## All images (8 diseases)

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 100.0 | 80.4 | 51.7 | 26.7 | 64.7 | 960 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 22.5 | 12.9 | 10.8 | 2.9 | 12.3 | 960 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 65.9 | 30.4 | 63.6 | 23.2 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 6.5 | 4.3 | 17.6 | 1.6 |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 12.5 | 25.0 | 18.8 | 25.0 | 52.1 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 2.1 | 0.0 | 2.1 | 8.3 | 2.1 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP database, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 45.8 | 49.3 | 46.5 | 43.8 | 79.2 |
| CLIP zero-shot, frozen clip-vit-large-patch14 (recomputed) [recipe B, 8 diseases] | 9.0 | 4.2 | 9.7 | 7.6 | 13.9 |

### Correct neighbours among the k database photos

| Level | Images | No correct neighbour | At least 1 correct (%) | Mean correct of k |
| --- | ---: | ---: | ---: | ---: |
| L0 | 240 | 0 | 100.0 | 4.9 |
| L1 | 240 | 26 | 89.2 | 3.8 |
| L2 | 240 | 59 | 75.4 | 2.5 |
| L3 | 240 | 119 | 50.4 | 1.4 |
| All | 960 | 204 | 78.8 | 3.1 |
