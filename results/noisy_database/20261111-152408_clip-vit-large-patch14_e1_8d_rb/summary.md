# E1: frozen CLIP + noisy copies in the database

Run folder: `results/noisy_database/20261111-152408_clip-vit-large-patch14_e1_8d_rb`

- database = 240 clean photos + 3600 noisy copies; k = 5; leave-one-photo-out
- share of the 5 neighbours that are noisy copies: L0 3%, L3 100%
- TEST SET: recipe B = the same photos, noise types and folds, with L1-L3 made by a different noise recipe (src/safecrop/noise_b.py). The Step 2 / 2b baselines were scored on the original images, so they are not shown or tested here.
- 8 DISEASES: black gram yellow mosaic is an 8th choice (30 photos, 120 images, its own folds). The 840 original images come first so they stay comparable (these methods could also answer black gram, an 8th option the earlier 7-disease runs did not have).

## The original images (7 diseases): comparable with every earlier number

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CLIP database + noisy copies (levels [1, 2, 3], x1) [recipe B, 8 diseases] | 100.0 | 96.7 | 91.4 | 67.1 | 88.8 | 840 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| CLIP database + noisy copies (levels [1, 2, 3], x1) [recipe B, 8 diseases] | 90.3 | 75.3 | 87.8 | 61.6 |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP database + noisy copies (levels [1, 2, 3], x1) [recipe B, 8 diseases] | 54.8 | 76.2 | 64.3 | 69.0 | 71.4 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP database + noisy copies (levels [1, 2, 3], x1) [recipe B, 8 diseases] | 81.7 | 91.3 | 81.7 | 83.3 | 87.3 |


## Black gram yellow mosaic only (no earlier baselines)

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CLIP database + noisy copies (levels [1, 2, 3], x1) [recipe B, 8 diseases] | 100.0 | 93.3 | 80.0 | 20.0 | 73.3 | 120 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| CLIP database + noisy copies (levels [1, 2, 3], x1) [recipe B, 8 diseases] | 73.3 | 20.0 | nan | nan |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP database + noisy copies (levels [1, 2, 3], x1) [recipe B, 8 diseases] | 0.0 | 33.3 | 16.7 | 16.7 | 33.3 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP database + noisy copies (levels [1, 2, 3], x1) [recipe B, 8 diseases] | 55.6 | 72.2 | 55.6 | 61.1 | 77.8 |

## All images (8 diseases)

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CLIP database + noisy copies (levels [1, 2, 3], x1) [recipe B, 8 diseases] | 100.0 | 96.2 | 90.0 | 61.3 | 86.9 | 960 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| CLIP database + noisy copies (levels [1, 2, 3], x1) [recipe B, 8 diseases] | 85.9 | 60.9 | 87.8 | 61.6 |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP database + noisy copies (levels [1, 2, 3], x1) [recipe B, 8 diseases] | 47.9 | 70.8 | 58.3 | 62.5 | 66.7 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP database + noisy copies (levels [1, 2, 3], x1) [recipe B, 8 diseases] | 78.5 | 88.9 | 78.5 | 80.6 | 86.1 |

### Correct neighbours among the k database photos

| Level | Images | No correct neighbour | At least 1 correct (%) | Mean correct of k |
| --- | ---: | ---: | ---: | ---: |
| L0 | 240 | 0 | 100.0 | 5.0 |
| L1 | 240 | 3 | 98.8 | 4.7 |
| L2 | 240 | 4 | 98.3 | 4.2 |
| L3 | 240 | 35 | 85.4 | 2.7 |
| All | 960 | 42 | 95.6 | 4.1 |
