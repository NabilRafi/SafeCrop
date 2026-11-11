# E3: fine-tuned CLIP

Run folder: `results/finetune/20261111-131836_clip-vit-large-patch14_e4_f0`

- folds [0] (5-fold cross-validation by photo; each image scored by a model that never saw its photo)
- model openai/clip-vit-large-patch14; unfreeze last 4 blocks; 15 epochs; lr 1e-05; consistency weight 1.0; noisy views 1 at levels [1, 2, 3]
- seconds per fold: {0: 167.5}
- PARTIAL: scored on 168 of 840 images; baselines below use the same images.

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies | 100.0 | 100.0 | 100.0 | 97.6 | 99.4 | 168 |
| Fine-tuned CLIP head (k4 e15 cons1.0) | 100.0 | 100.0 | 100.0 | 95.2 | 98.8 | 168 |
| CLIP database, frozen (Step 2) | 100.0 | 92.9 | 76.2 | 35.7 | 76.2 | 168 |
| Gemini + references + descriptions (Step 2b) | 100.0 | 92.9 | 81.0 | 40.5 | 78.6 | 168 |
| Gemini plain, 33 options (Step 2) | 64.3 | 42.9 | 16.7 | 9.5 | 33.3 | 168 |
| CLIP zero-shot, 33 options (Step 2) | 31.0 | 16.7 | 7.1 | 7.1 | 15.5 | 168 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies | 100.0 | 100.0 | 99.0 | 96.0 |
| Fine-tuned CLIP head (k4 e15 cons1.0) | 98.5 | 94.1 | 99.0 | 96.0 |
| CLIP database, frozen (Step 2) | 82.4 | 47.1 | 72.0 | 28.0 |
| Gemini + references + descriptions (Step 2b) | 79.4 | 41.2 | 78.0 | 40.0 |
| Gemini plain, 33 options (Step 2) | 48.5 | 23.5 | 23.0 | 0.0 |
| CLIP zero-shot, 33 options (Step 2) | 10.3 | 5.9 | 19.0 | 8.0 |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies | 100.0 | 100.0 | 100.0 | 100.0 | 87.5 |
| Fine-tuned CLIP head (k4 e15 cons1.0) | 100.0 | 100.0 | 87.5 | 100.0 | 87.5 |
| CLIP database, frozen (Step 2) | 40.0 | 25.0 | 25.0 | 50.0 | 37.5 |
| Gemini + references + descriptions (Step 2b) | 40.0 | 50.0 | 25.0 | 50.0 | 37.5 |
| Gemini plain, 33 options (Step 2) | 20.0 | 12.5 | 0.0 | 0.0 | 12.5 |
| CLIP zero-shot, 33 options (Step 2) | 10.0 | 0.0 | 0.0 | 25.0 | 0.0 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies | 100.0 | 100.0 | 100.0 | 100.0 | 95.8 |
| Fine-tuned CLIP head (k4 e15 cons1.0) | 100.0 | 100.0 | 95.8 | 100.0 | 95.8 |
| CLIP database, frozen (Step 2) | 66.7 | 75.0 | 58.3 | 75.0 | 66.7 |
| Gemini + references + descriptions (Step 2b) | 66.7 | 83.3 | 62.5 | 70.8 | 75.0 |
| Gemini plain, 33 options (Step 2) | 30.0 | 20.8 | 16.7 | 20.8 | 25.0 |
| CLIP zero-shot, 33 options (Step 2) | 10.0 | 16.7 | 0.0 | 20.8 | 4.2 |

### Head to head (McNemar exact test)

| New | Baseline | Levels | Images | Only new right | Only baseline right | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies | CLIP database, frozen (Step 2) | All | 168 | 39 | 0 | <0.001 |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies | CLIP database, frozen (Step 2) | L3 | 42 | 26 | 0 | <0.001 |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies | Gemini + references + descriptions (Step 2b) | All | 168 | 35 | 0 | <0.001 |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies | Gemini + references + descriptions (Step 2b) | L3 | 42 | 24 | 0 | <0.001 |
| Fine-tuned CLIP head (k4 e15 cons1.0) | CLIP database, frozen (Step 2) | All | 168 | 38 | 0 | <0.001 |
| Fine-tuned CLIP head (k4 e15 cons1.0) | CLIP database, frozen (Step 2) | L3 | 42 | 25 | 0 | <0.001 |
| Fine-tuned CLIP head (k4 e15 cons1.0) | Gemini + references + descriptions (Step 2b) | All | 168 | 34 | 0 | <0.001 |
| Fine-tuned CLIP head (k4 e15 cons1.0) | Gemini + references + descriptions (Step 2b) | L3 | 42 | 23 | 0 | <0.001 |

### Correct neighbours among the k database photos

| Level | Images | No correct neighbour | At least 1 correct (%) | Mean correct of k |
| --- | ---: | ---: | ---: | ---: |
| L0 | 42 | 0 | 100.0 | 5.0 |
| L1 | 42 | 0 | 100.0 | 5.0 |
| L2 | 42 | 0 | 100.0 | 5.0 |
| L3 | 42 | 1 | 97.6 | 4.7 |
| All | 168 | 1 | 99.4 | 4.9 |
