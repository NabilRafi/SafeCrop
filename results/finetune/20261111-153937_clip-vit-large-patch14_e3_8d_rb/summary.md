# E3: fine-tuned CLIP

Run folder: `results/finetune/20261111-153937_clip-vit-large-patch14_e3_8d_rb`

- folds [0, 1, 2, 3, 4] (5-fold cross-validation by photo; each image scored by a model that never saw its photo)
- model openai/clip-vit-large-patch14; unfreeze last 4 blocks; 15 epochs; lr 1e-05; consistency weight 1.0; noisy views 1 at levels [1, 2, 3]
- seconds per fold: {0: 124.4, 1: 121.8, 2: 121.7, 3: 121.8, 4: 121.8}
- the SAME trained models as run 20261111-152925_clip-vit-large-patch14_e3_8d (trained once on the test recipe's noise, scored on both test sets; seconds per fold include both)
- TEST SET: recipe B = the same photos, noise types and folds, with L1-L3 made by a different noise recipe (src/safecrop/noise_b.py). The Step 2 / 2b baselines were scored on the original images, so they are not shown or tested here.
- 8 DISEASES: black gram yellow mosaic is an 8th choice (30 photos, 120 images, its own folds). The 840 original images come first so they stay comparable (these methods could also answer black gram, an 8th option the earlier 7-disease runs did not have).

## The original images (7 diseases): comparable with every earlier number

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) [recipe B, 8 diseases] | 100.0 | 99.0 | 94.8 | 73.8 | 91.9 | 840 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [recipe B, 8 diseases] | 100.0 | 99.5 | 97.6 | 79.5 | 94.2 | 840 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) [recipe B, 8 diseases] | 96.8 | 90.6 | 88.6 | 62.4 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [recipe B, 8 diseases] | 97.1 | 90.6 | 92.2 | 72.0 |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) [recipe B, 8 diseases] | 38.1 | 81.0 | 81.0 | 71.4 | 97.6 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [recipe B, 8 diseases] | 42.9 | 85.7 | 88.1 | 83.3 | 97.6 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) [recipe B, 8 diseases] | 77.8 | 91.3 | 92.1 | 85.7 | 99.2 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [recipe B, 8 diseases] | 80.2 | 94.4 | 95.2 | 92.1 | 99.2 |


## Black gram yellow mosaic only (no earlier baselines)

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) [recipe B, 8 diseases] | 100.0 | 96.7 | 93.3 | 63.3 | 88.3 | 120 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [recipe B, 8 diseases] | 100.0 | 96.7 | 96.7 | 73.3 | 91.7 | 120 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) [recipe B, 8 diseases] | 88.3 | 63.3 | nan | nan |
| Fine-tuned CLIP head (k4 e15 cons1.0) [recipe B, 8 diseases] | 91.7 | 73.3 | nan | nan |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) [recipe B, 8 diseases] | 33.3 | 100.0 | 33.3 | 66.7 | 83.3 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [recipe B, 8 diseases] | 33.3 | 100.0 | 66.7 | 83.3 | 83.3 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) [recipe B, 8 diseases] | 61.1 | 100.0 | 77.8 | 88.9 | 94.4 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [recipe B, 8 diseases] | 66.7 | 100.0 | 88.9 | 94.4 | 94.4 |

## All images (8 diseases)

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) [recipe B, 8 diseases] | 100.0 | 98.8 | 94.6 | 72.5 | 91.5 | 960 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [recipe B, 8 diseases] | 100.0 | 99.2 | 97.5 | 78.8 | 93.9 | 960 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) [recipe B, 8 diseases] | 94.6 | 83.5 | 88.6 | 62.4 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [recipe B, 8 diseases] | 95.7 | 86.1 | 92.2 | 72.0 |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) [recipe B, 8 diseases] | 37.5 | 83.3 | 75.0 | 70.8 | 95.8 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [recipe B, 8 diseases] | 41.7 | 87.5 | 85.4 | 83.3 | 95.8 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) [recipe B, 8 diseases] | 75.7 | 92.4 | 90.3 | 86.1 | 98.6 |
| Fine-tuned CLIP head (k4 e15 cons1.0) [recipe B, 8 diseases] | 78.5 | 95.1 | 94.4 | 92.4 | 98.6 |

### Correct neighbours among the k database photos

| Level | Images | No correct neighbour | At least 1 correct (%) | Mean correct of k |
| --- | ---: | ---: | ---: | ---: |
| L0 | 240 | 0 | 100.0 | 5.0 |
| L1 | 240 | 2 | 99.2 | 4.9 |
| L2 | 240 | 7 | 97.1 | 4.7 |
| L3 | 240 | 48 | 80.0 | 3.5 |
| All | 960 | 57 | 94.1 | 4.5 |
