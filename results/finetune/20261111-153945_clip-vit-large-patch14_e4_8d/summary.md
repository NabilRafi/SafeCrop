# E3: fine-tuned CLIP

Run folder: `results/finetune/20261111-153945_clip-vit-large-patch14_e4_8d`

- folds [0, 1, 2, 3, 4] (5-fold cross-validation by photo; each image scored by a model that never saw its photo)
- model openai/clip-vit-large-patch14; unfreeze last 4 blocks; 15 epochs; lr 1e-05; consistency weight 1.0; noisy views 1 at levels [1, 2, 3]
- seconds per fold: {0: 284.5, 1: 276.5, 2: 276.8, 3: 278.4, 4: 275.8}
- 8 DISEASES: black gram yellow mosaic is an 8th choice (30 photos, 120 images, its own folds). The 840 original images come first so they stay comparable (these methods could also answer black gram, an 8th option the earlier 7-disease runs did not have).

## The original images (7 diseases): comparable with every earlier number

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies [8 diseases] | 100.0 | 100.0 | 99.0 | 96.7 | 98.9 | 840 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [8 diseases] | 100.0 | 100.0 | 99.5 | 94.3 | 98.5 | 840 |
| CLIP database, frozen (Step 2) | 100.0 | 93.3 | 71.9 | 40.0 | 76.3 | 840 |
| Gemini + references + descriptions (Step 2b) | 100.0 | 92.9 | 75.2 | 47.1 | 78.8 | 840 |
| Gemini plain, 33 options (Step 2) | 66.7 | 48.6 | 26.2 | 12.9 | 38.6 | 840 |
| CLIP zero-shot, 33 options (Step 2) | 25.7 | 15.2 | 8.6 | 3.8 | 13.3 | 840 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies [8 diseases] | 98.8 | 96.5 | 99.0 | 96.8 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [8 diseases] | 97.9 | 91.8 | 98.8 | 96.0 |
| CLIP database, frozen (Step 2) | 81.2 | 48.2 | 73.0 | 34.4 |
| Gemini + references + descriptions (Step 2b) | 80.6 | 48.2 | 77.6 | 46.4 |
| Gemini plain, 33 options (Step 2) | 54.7 | 29.4 | 27.6 | 1.6 |
| CLIP zero-shot, 33 options (Step 2) | 9.1 | 3.5 | 16.2 | 4.0 |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies [8 diseases] | 90.5 | 100.0 | 97.6 | 97.6 | 97.6 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [8 diseases] | 90.5 | 100.0 | 90.5 | 97.6 | 92.9 |
| CLIP database, frozen (Step 2) | 26.2 | 33.3 | 28.6 | 54.8 | 57.1 |
| Gemini + references + descriptions (Step 2b) | 31.0 | 52.4 | 38.1 | 52.4 | 61.9 |
| Gemini plain, 33 options (Step 2) | 9.5 | 14.3 | 14.3 | 4.8 | 21.4 |
| CLIP zero-shot, 33 options (Step 2) | 4.8 | 0.0 | 0.0 | 11.9 | 2.4 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies [8 diseases] | 96.8 | 100.0 | 98.4 | 98.4 | 99.2 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [8 diseases] | 96.8 | 100.0 | 96.0 | 99.2 | 97.6 |
| CLIP database, frozen (Step 2) | 61.1 | 70.6 | 61.9 | 70.6 | 77.8 |
| Gemini + references + descriptions (Step 2b) | 61.1 | 78.6 | 65.9 | 69.0 | 84.1 |
| Gemini plain, 33 options (Step 2) | 25.4 | 34.9 | 26.2 | 19.0 | 40.5 |
| CLIP zero-shot, 33 options (Step 2) | 5.6 | 9.5 | 7.1 | 16.7 | 7.1 |

### Head to head (McNemar exact test)

| New | Baseline | Levels | Images | Only new right | Only baseline right | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies [8 diseases] | CLIP database, frozen (Step 2) | All | 840 | 191 | 1 | <0.001 |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies [8 diseases] | CLIP database, frozen (Step 2) | L3 | 210 | 120 | 1 | <0.001 |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies [8 diseases] | Gemini + references + descriptions (Step 2b) | All | 840 | 171 | 2 | <0.001 |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies [8 diseases] | Gemini + references + descriptions (Step 2b) | L3 | 210 | 105 | 1 | <0.001 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [8 diseases] | CLIP database, frozen (Step 2) | All | 840 | 187 | 1 | <0.001 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [8 diseases] | CLIP database, frozen (Step 2) | L3 | 210 | 115 | 1 | <0.001 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [8 diseases] | Gemini + references + descriptions (Step 2b) | All | 840 | 166 | 1 | <0.001 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [8 diseases] | Gemini + references + descriptions (Step 2b) | L3 | 210 | 100 | 1 | <0.001 |

## Black gram yellow mosaic only (no earlier baselines)

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies [8 diseases] | 100.0 | 96.7 | 96.7 | 90.0 | 95.8 | 120 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [8 diseases] | 100.0 | 96.7 | 96.7 | 93.3 | 96.7 | 120 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies [8 diseases] | 95.8 | 90.0 | nan | nan |
| Fine-tuned CLIP head (k4 e15 cons1.0) [8 diseases] | 96.7 | 93.3 | nan | nan |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies [8 diseases] | 50.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [8 diseases] | 66.7 | 100.0 | 100.0 | 100.0 | 100.0 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies [8 diseases] | 72.2 | 100.0 | 100.0 | 100.0 | 100.0 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [8 diseases] | 77.8 | 100.0 | 100.0 | 100.0 | 100.0 |

## All images (8 diseases)

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies [8 diseases] | 100.0 | 99.6 | 98.8 | 95.8 | 98.5 | 960 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [8 diseases] | 100.0 | 99.6 | 99.2 | 94.2 | 98.2 | 960 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies [8 diseases] | 98.0 | 94.8 | 99.0 | 96.8 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [8 diseases] | 97.6 | 92.2 | 98.8 | 96.0 |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies [8 diseases] | 85.4 | 100.0 | 97.9 | 97.9 | 97.9 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [8 diseases] | 87.5 | 100.0 | 91.7 | 97.9 | 93.8 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies [8 diseases] | 93.8 | 100.0 | 98.6 | 98.6 | 99.3 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [8 diseases] | 94.4 | 100.0 | 96.5 | 99.3 | 97.9 |

### Correct neighbours among the k database photos

| Level | Images | No correct neighbour | At least 1 correct (%) | Mean correct of k |
| --- | ---: | ---: | ---: | ---: |
| L0 | 240 | 0 | 100.0 | 5.0 |
| L1 | 240 | 0 | 100.0 | 5.0 |
| L2 | 240 | 1 | 99.6 | 4.9 |
| L3 | 240 | 3 | 98.8 | 4.7 |
| All | 960 | 4 | 99.6 | 4.9 |
