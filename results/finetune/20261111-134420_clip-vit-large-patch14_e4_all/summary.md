# E3: fine-tuned CLIP

Run folder: `results/finetune/20261111-134420_clip-vit-large-patch14_e4_all`

- folds [0, 1, 2, 3, 4] (5-fold cross-validation by photo; each image scored by a model that never saw its photo)
- model openai/clip-vit-large-patch14; unfreeze last 4 blocks; 15 epochs; lr 1e-05; consistency weight 1.0; noisy views 1 at levels [1, 2, 3]
- seconds per fold: {0: 163.8, 1: 159.7, 2: 159.3, 3: 162.2, 4: 160.7}

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies | 100.0 | 100.0 | 99.5 | 97.1 | 99.2 | 840 |
| Fine-tuned CLIP head (k4 e15 cons1.0) | 100.0 | 100.0 | 99.5 | 95.2 | 98.7 | 840 |
| CLIP database, frozen (Step 2) | 100.0 | 93.3 | 71.9 | 40.0 | 76.3 | 840 |
| Gemini + references + descriptions (Step 2b) | 100.0 | 92.9 | 75.2 | 47.1 | 78.8 | 840 |
| Gemini plain, 33 options (Step 2) | 66.7 | 48.6 | 26.2 | 12.9 | 38.6 | 840 |
| CLIP zero-shot, 33 options (Step 2) | 25.7 | 15.2 | 8.6 | 3.8 | 13.3 | 840 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies | 99.4 | 97.6 | 99.0 | 96.8 |
| Fine-tuned CLIP head (k4 e15 cons1.0) | 98.8 | 95.3 | 98.6 | 95.2 |
| CLIP database, frozen (Step 2) | 81.2 | 48.2 | 73.0 | 34.4 |
| Gemini + references + descriptions (Step 2b) | 80.6 | 48.2 | 77.6 | 46.4 |
| Gemini plain, 33 options (Step 2) | 54.7 | 29.4 | 27.6 | 1.6 |
| CLIP zero-shot, 33 options (Step 2) | 9.1 | 3.5 | 16.2 | 4.0 |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies | 92.9 | 100.0 | 97.6 | 97.6 | 97.6 |
| Fine-tuned CLIP head (k4 e15 cons1.0) | 92.9 | 100.0 | 90.5 | 97.6 | 95.2 |
| CLIP database, frozen (Step 2) | 26.2 | 33.3 | 28.6 | 54.8 | 57.1 |
| Gemini + references + descriptions (Step 2b) | 31.0 | 52.4 | 38.1 | 52.4 | 61.9 |
| Gemini plain, 33 options (Step 2) | 9.5 | 14.3 | 14.3 | 4.8 | 21.4 |
| CLIP zero-shot, 33 options (Step 2) | 4.8 | 0.0 | 0.0 | 11.9 | 2.4 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies | 97.6 | 100.0 | 98.4 | 99.2 | 99.2 |
| Fine-tuned CLIP head (k4 e15 cons1.0) | 97.6 | 100.0 | 96.0 | 99.2 | 98.4 |
| CLIP database, frozen (Step 2) | 61.1 | 70.6 | 61.9 | 70.6 | 77.8 |
| Gemini + references + descriptions (Step 2b) | 61.1 | 78.6 | 65.9 | 69.0 | 84.1 |
| Gemini plain, 33 options (Step 2) | 25.4 | 34.9 | 26.2 | 19.0 | 40.5 |
| CLIP zero-shot, 33 options (Step 2) | 5.6 | 9.5 | 7.1 | 16.7 | 7.1 |

### Head to head (McNemar exact test)

| New | Baseline | Levels | Images | Only new right | Only baseline right | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies | CLIP database, frozen (Step 2) | All | 840 | 193 | 1 | <0.001 |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies | CLIP database, frozen (Step 2) | L3 | 210 | 121 | 1 | <0.001 |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies | Gemini + references + descriptions (Step 2b) | All | 840 | 172 | 1 | <0.001 |
| Fine-tuned CLIP database (k4 e15 cons1.0) + noisy copies | Gemini + references + descriptions (Step 2b) | L3 | 210 | 106 | 1 | <0.001 |
| Fine-tuned CLIP head (k4 e15 cons1.0) | CLIP database, frozen (Step 2) | All | 840 | 189 | 1 | <0.001 |
| Fine-tuned CLIP head (k4 e15 cons1.0) | CLIP database, frozen (Step 2) | L3 | 210 | 117 | 1 | <0.001 |
| Fine-tuned CLIP head (k4 e15 cons1.0) | Gemini + references + descriptions (Step 2b) | All | 840 | 168 | 1 | <0.001 |
| Fine-tuned CLIP head (k4 e15 cons1.0) | Gemini + references + descriptions (Step 2b) | L3 | 210 | 102 | 1 | <0.001 |

### Correct neighbours among the k database photos

| Level | Images | No correct neighbour | At least 1 correct (%) | Mean correct of k |
| --- | ---: | ---: | ---: | ---: |
| L0 | 210 | 0 | 100.0 | 5.0 |
| L1 | 210 | 0 | 100.0 | 5.0 |
| L2 | 210 | 0 | 100.0 | 5.0 |
| L3 | 210 | 3 | 98.6 | 4.7 |
| All | 840 | 3 | 99.6 | 4.9 |
