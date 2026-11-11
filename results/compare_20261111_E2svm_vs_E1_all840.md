Images compared: 840 of 840

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E2 SVM, frozen + noisy copies | 100.0 | 99.5 | 99.0 | 97.6 | 99.0 | 840 |
| E1 frozen + noisy copies (database) | 100.0 | 100.0 | 99.0 | 95.2 | 98.6 | 840 |
| CLIP database, frozen (Step 2) | 100.0 | 93.3 | 71.9 | 40.0 | 76.3 | 840 |
| Gemini + references + descriptions (Step 2b) | 100.0 | 92.9 | 75.2 | 47.1 | 78.8 | 840 |
| Gemini plain, 33 options (Step 2) | 66.7 | 48.6 | 26.2 | 12.9 | 38.6 | 840 |
| CLIP zero-shot, 33 options (Step 2) | 25.7 | 15.2 | 8.6 | 3.8 | 13.3 | 840 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| E2 SVM, frozen + noisy copies | 99.4 | 97.6 | 98.8 | 97.6 |
| E1 frozen + noisy copies (database) | 98.8 | 95.3 | 98.4 | 95.2 |
| CLIP database, frozen (Step 2) | 81.2 | 48.2 | 73.0 | 34.4 |
| Gemini + references + descriptions (Step 2b) | 80.6 | 48.2 | 77.6 | 46.4 |
| Gemini plain, 33 options (Step 2) | 54.7 | 29.4 | 27.6 | 1.6 |
| CLIP zero-shot, 33 options (Step 2) | 9.1 | 3.5 | 16.2 | 4.0 |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| E2 SVM, frozen + noisy copies | 92.9 | 100.0 | 100.0 | 100.0 | 95.2 |
| E1 frozen + noisy copies (database) | 85.7 | 100.0 | 95.2 | 100.0 | 95.2 |
| CLIP database, frozen (Step 2) | 26.2 | 33.3 | 28.6 | 54.8 | 57.1 |
| Gemini + references + descriptions (Step 2b) | 31.0 | 52.4 | 38.1 | 52.4 | 61.9 |
| Gemini plain, 33 options (Step 2) | 9.5 | 14.3 | 14.3 | 4.8 | 21.4 |
| CLIP zero-shot, 33 options (Step 2) | 4.8 | 0.0 | 0.0 | 11.9 | 2.4 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| E2 SVM, frozen + noisy copies | 97.6 | 100.0 | 97.6 | 100.0 | 98.4 |
| E1 frozen + noisy copies (database) | 95.2 | 100.0 | 97.6 | 99.2 | 98.4 |
| CLIP database, frozen (Step 2) | 61.1 | 70.6 | 61.9 | 70.6 | 77.8 |
| Gemini + references + descriptions (Step 2b) | 61.1 | 78.6 | 65.9 | 69.0 | 84.1 |
| Gemini plain, 33 options (Step 2) | 25.4 | 34.9 | 26.2 | 19.0 | 40.5 |
| CLIP zero-shot, 33 options (Step 2) | 5.6 | 9.5 | 7.1 | 16.7 | 7.1 |

### Head to head (McNemar exact test)

| New | Baseline | Levels | Images | Only new right | Only baseline right | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E2 SVM, frozen + noisy copies | CLIP database, frozen (Step 2) | All | 840 | 194 | 3 | <0.001 |
| E2 SVM, frozen + noisy copies | CLIP database, frozen (Step 2) | L3 | 210 | 123 | 2 | <0.001 |
| E2 SVM, frozen + noisy copies | Gemini + references + descriptions (Step 2b) | All | 840 | 173 | 3 | <0.001 |
| E2 SVM, frozen + noisy copies | Gemini + references + descriptions (Step 2b) | L3 | 210 | 108 | 2 | <0.001 |
| E1 frozen + noisy copies (database) | CLIP database, frozen (Step 2) | All | 840 | 192 | 5 | <0.001 |
| E1 frozen + noisy copies (database) | CLIP database, frozen (Step 2) | L3 | 210 | 120 | 4 | <0.001 |
| E1 frozen + noisy copies (database) | Gemini + references + descriptions (Step 2b) | All | 840 | 172 | 6 | <0.001 |
| E1 frozen + noisy copies (database) | Gemini + references + descriptions (Step 2b) | L3 | 210 | 106 | 5 | <0.001 |

### Head to head (McNemar exact test)

| New | Baseline | Levels | Images | Only new right | Only baseline right | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E2 SVM, frozen + noisy copies | E1 frozen + noisy copies (database) | All | 840 | 7 | 3 | 0.344 |
| E2 SVM, frozen + noisy copies | E1 frozen + noisy copies (database) | L3 | 210 | 6 | 1 | 0.125 |
