# E2: SVM on frozen CLIP (clean + noisy copies)

Run folder: `results/linear_probe/20261111-152918_clip-vit-large-patch14_svm_8d_rb`

- 5-fold cross-validation by photo (folds fixed in data/manifest.csv)
- RBF SVM; C per fold {0: 10.0, 1: 10.0, 2: 10.0, 3: 10.0, 4: 10.0} (chosen by 4-fold CV inside the training photos); classes = the 8 test diseases
- TEST SET: recipe B = the same photos, noise types and folds, with L1-L3 made by a different noise recipe (src/safecrop/noise_b.py). The Step 2 / 2b baselines were scored on the original images, so they are not shown or tested here.
- 8 DISEASES: black gram yellow mosaic is an 8th choice (30 photos, 120 images, its own folds). The 840 original images come first so they stay comparable (these methods could also answer black gram, an 8th option the earlier 7-disease runs did not have).

## The original images (7 diseases): comparable with every earlier number

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [recipe B, 8 diseases] | 99.5 | 99.0 | 97.1 | 78.1 | 93.5 | 840 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [recipe B, 8 diseases] | 96.2 | 88.2 | 91.6 | 71.2 |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [recipe B, 8 diseases] | 54.8 | 90.5 | 83.3 | 78.6 | 83.3 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [recipe B, 8 diseases] | 84.1 | 96.0 | 92.9 | 90.5 | 93.7 |


## Black gram yellow mosaic only (no earlier baselines)

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [recipe B, 8 diseases] | 100.0 | 93.3 | 93.3 | 70.0 | 89.2 | 120 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [recipe B, 8 diseases] | 89.2 | 70.0 | nan | nan |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [recipe B, 8 diseases] | 50.0 | 66.7 | 50.0 | 83.3 | 100.0 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [recipe B, 8 diseases] | 83.3 | 88.9 | 77.8 | 77.8 | 100.0 |

## All images (8 diseases)

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [recipe B, 8 diseases] | 99.6 | 98.3 | 96.7 | 77.1 | 92.9 | 960 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [recipe B, 8 diseases] | 94.3 | 83.5 | 91.6 | 71.2 |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [recipe B, 8 diseases] | 54.2 | 87.5 | 79.2 | 79.2 | 85.4 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [recipe B, 8 diseases] | 84.0 | 95.1 | 91.0 | 88.9 | 94.4 |

