# E1: frozen CLIP + noisy copies in the database

Run folder: `results/noisy_database/20261111-120939_clip-vit-large-patch14_e1`

- database = 210 clean photos + 3150 noisy copies; k = 5; leave-one-photo-out
- share of the 5 neighbours that are noisy copies: L0 4%, L3 100%

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CLIP database + noisy copies (levels [1, 2, 3], x1) | 100.0 | 100.0 | 99.0 | 95.2 | 98.6 | 840 |
| CLIP database, frozen (Step 2) | 100.0 | 93.3 | 71.9 | 40.0 | 76.3 | 840 |
| Gemini + references + descriptions (Step 2b) | 100.0 | 92.9 | 75.2 | 47.1 | 78.8 | 840 |
| Gemini plain, 33 options (Step 2) | 66.7 | 48.6 | 26.2 | 12.9 | 38.6 | 840 |
| CLIP zero-shot, 33 options (Step 2) | 25.7 | 15.2 | 8.6 | 3.8 | 13.3 | 840 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| CLIP database + noisy copies (levels [1, 2, 3], x1) | 98.8 | 95.3 | 98.4 | 95.2 |
| CLIP database, frozen (Step 2) | 81.2 | 48.2 | 73.0 | 34.4 |
| Gemini + references + descriptions (Step 2b) | 80.6 | 48.2 | 77.6 | 46.4 |
| Gemini plain, 33 options (Step 2) | 54.7 | 29.4 | 27.6 | 1.6 |
| CLIP zero-shot, 33 options (Step 2) | 9.1 | 3.5 | 16.2 | 4.0 |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP database + noisy copies (levels [1, 2, 3], x1) | 85.7 | 100.0 | 95.2 | 100.0 | 95.2 |
| CLIP database, frozen (Step 2) | 26.2 | 33.3 | 28.6 | 54.8 | 57.1 |
| Gemini + references + descriptions (Step 2b) | 31.0 | 52.4 | 38.1 | 52.4 | 61.9 |
| Gemini plain, 33 options (Step 2) | 9.5 | 14.3 | 14.3 | 4.8 | 21.4 |
| CLIP zero-shot, 33 options (Step 2) | 4.8 | 0.0 | 0.0 | 11.9 | 2.4 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP database + noisy copies (levels [1, 2, 3], x1) | 95.2 | 100.0 | 97.6 | 99.2 | 98.4 |
| CLIP database, frozen (Step 2) | 61.1 | 70.6 | 61.9 | 70.6 | 77.8 |
| Gemini + references + descriptions (Step 2b) | 61.1 | 78.6 | 65.9 | 69.0 | 84.1 |
| Gemini plain, 33 options (Step 2) | 25.4 | 34.9 | 26.2 | 19.0 | 40.5 |
| CLIP zero-shot, 33 options (Step 2) | 5.6 | 9.5 | 7.1 | 16.7 | 7.1 |

### Head to head (McNemar exact test)

| New | Baseline | Levels | Images | Only new right | Only baseline right | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CLIP database + noisy copies (levels [1, 2, 3], x1) | CLIP database, frozen (Step 2) | All | 840 | 192 | 5 | <0.001 |
| CLIP database + noisy copies (levels [1, 2, 3], x1) | CLIP database, frozen (Step 2) | L3 | 210 | 120 | 4 | <0.001 |
| CLIP database + noisy copies (levels [1, 2, 3], x1) | Gemini + references + descriptions (Step 2b) | All | 840 | 172 | 6 | <0.001 |
| CLIP database + noisy copies (levels [1, 2, 3], x1) | Gemini + references + descriptions (Step 2b) | L3 | 210 | 106 | 5 | <0.001 |

### Correct neighbours among the k database photos

| Level | Images | No correct neighbour | At least 1 correct (%) | Mean correct of k |
| --- | ---: | ---: | ---: | ---: |
| L0 | 210 | 0 | 100.0 | 5.0 |
| L1 | 210 | 0 | 100.0 | 5.0 |
| L2 | 210 | 0 | 100.0 | 4.8 |
| L3 | 210 | 1 | 99.5 | 4.4 |
| All | 840 | 1 | 99.9 | 4.8 |
