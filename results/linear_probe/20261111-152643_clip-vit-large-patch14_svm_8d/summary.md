# E2: SVM on frozen CLIP (clean + noisy copies)

Run folder: `results/linear_probe/20261111-152643_clip-vit-large-patch14_svm_8d`

- 5-fold cross-validation by photo (folds fixed in data/manifest.csv)
- RBF SVM; C per fold {0: 10.0, 1: 10.0, 2: 10.0, 3: 10.0, 4: 10.0} (chosen by 4-fold CV inside the training photos); classes = the 8 test diseases
- 8 DISEASES: black gram yellow mosaic is an 8th choice (30 photos, 120 images, its own folds). The 840 original images come first so they stay comparable (these methods could also answer black gram, an 8th option the earlier 7-disease runs did not have).

## The original images (7 diseases): comparable with every earlier number

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [8 diseases] | 99.5 | 99.5 | 98.6 | 97.1 | 98.7 | 840 |
| CLIP database, frozen (Step 2) | 100.0 | 93.3 | 71.9 | 40.0 | 76.3 | 840 |
| Gemini + references + descriptions (Step 2b) | 100.0 | 92.9 | 75.2 | 47.1 | 78.8 | 840 |
| Gemini plain, 33 options (Step 2) | 66.7 | 48.6 | 26.2 | 12.9 | 38.6 | 840 |
| CLIP zero-shot, 33 options (Step 2) | 25.7 | 15.2 | 8.6 | 3.8 | 13.3 | 840 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [8 diseases] | 99.4 | 97.6 | 98.2 | 96.8 |
| CLIP database, frozen (Step 2) | 81.2 | 48.2 | 73.0 | 34.4 |
| Gemini + references + descriptions (Step 2b) | 80.6 | 48.2 | 77.6 | 46.4 |
| Gemini plain, 33 options (Step 2) | 54.7 | 29.4 | 27.6 | 1.6 |
| CLIP zero-shot, 33 options (Step 2) | 9.1 | 3.5 | 16.2 | 4.0 |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [8 diseases] | 90.5 | 100.0 | 100.0 | 100.0 | 95.2 |
| CLIP database, frozen (Step 2) | 26.2 | 33.3 | 28.6 | 54.8 | 57.1 |
| Gemini + references + descriptions (Step 2b) | 31.0 | 52.4 | 38.1 | 52.4 | 61.9 |
| Gemini plain, 33 options (Step 2) | 9.5 | 14.3 | 14.3 | 4.8 | 21.4 |
| CLIP zero-shot, 33 options (Step 2) | 4.8 | 0.0 | 0.0 | 11.9 | 2.4 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [8 diseases] | 96.8 | 100.0 | 97.6 | 99.2 | 98.4 |
| CLIP database, frozen (Step 2) | 61.1 | 70.6 | 61.9 | 70.6 | 77.8 |
| Gemini + references + descriptions (Step 2b) | 61.1 | 78.6 | 65.9 | 69.0 | 84.1 |
| Gemini plain, 33 options (Step 2) | 25.4 | 34.9 | 26.2 | 19.0 | 40.5 |
| CLIP zero-shot, 33 options (Step 2) | 5.6 | 9.5 | 7.1 | 16.7 | 7.1 |

### Head to head (McNemar exact test)

| New | Baseline | Levels | Images | Only new right | Only baseline right | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [8 diseases] | CLIP database, frozen (Step 2) | All | 840 | 192 | 4 | <0.001 |
| SVM on frozen CLIP (clean + noisy copies) [8 diseases] | CLIP database, frozen (Step 2) | L3 | 210 | 122 | 2 | <0.001 |
| SVM on frozen CLIP (clean + noisy copies) [8 diseases] | Gemini + references + descriptions (Step 2b) | All | 840 | 171 | 4 | <0.001 |
| SVM on frozen CLIP (clean + noisy copies) [8 diseases] | Gemini + references + descriptions (Step 2b) | L3 | 210 | 107 | 2 | <0.001 |

## Black gram yellow mosaic only (no earlier baselines)

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [8 diseases] | 100.0 | 100.0 | 100.0 | 96.7 | 99.2 | 120 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [8 diseases] | 99.2 | 96.7 | nan | nan |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [8 diseases] | 100.0 | 100.0 | 100.0 | 83.3 | 100.0 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [8 diseases] | 100.0 | 100.0 | 100.0 | 94.4 | 100.0 |

## All images (8 diseases)

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [8 diseases] | 99.6 | 99.6 | 98.8 | 97.1 | 98.8 | 960 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [8 diseases] | 99.3 | 97.4 | 98.2 | 96.8 |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [8 diseases] | 91.7 | 100.0 | 100.0 | 97.9 | 95.8 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| SVM on frozen CLIP (clean + noisy copies) [8 diseases] | 97.2 | 100.0 | 97.9 | 98.6 | 98.6 |

