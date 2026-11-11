# Robustness: test recipe vs recipe B (noise made a different way)

Images compared: 960 of 960 per test set (only images that every file scored).
Recipe B: same photos, noise types, levels and folds; each level matched to the test images' damage (levelled colour MS-SSIM). Every method learned or built its references from the TEST recipe's noise only.

## Accuracy drop from the test recipe to recipe B (paired McNemar: same photo, same level)

| Method | Levels | Test recipe % | Recipe B % | Change | Images | Only B right | Only test right | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| E0 frozen database (7 diseases) | L3 | 40.0 | 30.5 | -9.5 | 210 | 8 | 28 | 0.001 |
| E0 frozen database (7 diseases) | All | 76.3 | 67.9 | -8.4 | 840 | 22 | 93 | <0.001 |
| E0 frozen database (black gram) | L3 | 6.7 | 0.0 | -6.7 | 30 | 0 | 2 | 0.500 |
| E0 frozen database (black gram) | All | 48.3 | 42.5 | -5.8 | 120 | 1 | 8 | 0.039 |
| E0 CLIP zero-shot (7 diseases) | L3 | 3.8 | 1.4 | -2.4 | 210 | 2 | 7 | 0.180 |
| E0 CLIP zero-shot (7 diseases) | All | 13.3 | 13.0 | -0.3 | 840 | 35 | 38 | 0.815 |
| E0 CLIP zero-shot (black gram) | L3 | 10.0 | 13.3 | 3.3 | 30 | 4 | 3 | 1.000 |
| E0 CLIP zero-shot (black gram) | All | 5.0 | 7.5 | 2.5 | 120 | 6 | 3 | 0.508 |
| E1 frozen + noisy copies (7 diseases) | L3 | 95.7 | 67.1 | -28.6 | 210 | 5 | 65 | <0.001 |
| E1 frozen + noisy copies (7 diseases) | All | 98.6 | 88.8 | -9.8 | 840 | 7 | 89 | <0.001 |
| E1 frozen + noisy copies (black gram) | L3 | 90.0 | 20.0 | -70.0 | 30 | 0 | 21 | <0.001 |
| E1 frozen + noisy copies (black gram) | All | 93.3 | 73.3 | -20.0 | 120 | 2 | 26 | <0.001 |
| E2 SVM + noisy copies (7 diseases) | L3 | 97.1 | 78.1 | -19.0 | 210 | 4 | 44 | <0.001 |
| E2 SVM + noisy copies (7 diseases) | All | 98.7 | 93.5 | -5.2 | 840 | 6 | 50 | <0.001 |
| E2 SVM + noisy copies (black gram) | L3 | 96.7 | 70.0 | -26.7 | 30 | 1 | 9 | 0.021 |
| E2 SVM + noisy copies (black gram) | All | 99.2 | 89.2 | -10.0 | 120 | 1 | 13 | 0.002 |
| E3 fine-tuned, database (7 diseases) | L3 | 92.4 | 73.8 | -18.6 | 210 | 7 | 46 | <0.001 |
| E3 fine-tuned, database (7 diseases) | All | 98.0 | 91.9 | -6.1 | 840 | 7 | 58 | <0.001 |
| E3 fine-tuned, database (black gram) | L3 | 80.0 | 63.3 | -16.7 | 30 | 1 | 6 | 0.125 |
| E3 fine-tuned, database (black gram) | All | 92.5 | 88.3 | -4.2 | 120 | 2 | 7 | 0.180 |
| E3 fine-tuned, head (7 diseases) | L3 | 94.3 | 79.5 | -14.8 | 210 | 5 | 36 | <0.001 |
| E3 fine-tuned, head (7 diseases) | All | 98.5 | 94.2 | -4.3 | 840 | 5 | 41 | <0.001 |
| E3 fine-tuned, head (black gram) | L3 | 93.3 | 73.3 | -20.0 | 30 | 1 | 7 | 0.070 |
| E3 fine-tuned, head (black gram) | All | 96.7 | 91.7 | -5.0 | 120 | 1 | 7 | 0.070 |
| E4 fine-tuned + noisy copies (7 diseases) | L3 | 96.7 | 85.2 | -11.5 | 210 | 5 | 29 | <0.001 |
| E4 fine-tuned + noisy copies (7 diseases) | All | 98.9 | 95.4 | -3.5 | 840 | 6 | 36 | <0.001 |
| E4 fine-tuned + noisy copies (black gram) | L3 | 90.0 | 76.7 | -13.3 | 30 | 2 | 6 | 0.289 |
| E4 fine-tuned + noisy copies (black gram) | All | 95.8 | 92.5 | -3.3 | 120 | 2 | 6 | 0.289 |

## Recipe B (7 diseases): the usual tables

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E0 frozen database [recipe B] | 100.0 | 85.2 | 55.7 | 30.5 | 67.9 | 840 |
| E0 CLIP zero-shot [recipe B] | 25.7 | 14.3 | 10.5 | 1.4 | 13.0 | 840 |
| E1 frozen + noisy copies [recipe B] | 100.0 | 96.7 | 91.4 | 67.1 | 88.8 | 840 |
| E2 SVM + noisy copies [recipe B] | 99.5 | 99.0 | 97.1 | 78.1 | 93.5 | 840 |
| E3 fine-tuned, database [recipe B] | 100.0 | 99.0 | 94.8 | 73.8 | 91.9 | 840 |
| E3 fine-tuned, head [recipe B] | 100.0 | 99.5 | 97.6 | 79.5 | 94.2 | 840 |
| E4 fine-tuned + noisy copies [recipe B] | 100.0 | 99.0 | 97.1 | 85.2 | 95.4 | 840 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| E0 frozen database [recipe B] | 74.1 | 41.2 | 63.6 | 23.2 |
| E0 CLIP zero-shot [recipe B] | 6.2 | 1.2 | 17.6 | 1.6 |
| E1 frozen + noisy copies [recipe B] | 90.3 | 75.3 | 87.8 | 61.6 |
| E2 SVM + noisy copies [recipe B] | 96.2 | 88.2 | 91.6 | 71.2 |
| E3 fine-tuned, database [recipe B] | 96.8 | 90.6 | 88.6 | 62.4 |
| E3 fine-tuned, head [recipe B] | 97.1 | 90.6 | 92.2 | 72.0 |
| E4 fine-tuned + noisy copies [recipe B] | 98.2 | 95.3 | 93.4 | 78.4 |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| E0 frozen database [recipe B] | 14.3 | 28.6 | 21.4 | 28.6 | 59.5 |
| E0 CLIP zero-shot [recipe B] | 0.0 | 0.0 | 0.0 | 4.8 | 2.4 |
| E1 frozen + noisy copies [recipe B] | 54.8 | 76.2 | 64.3 | 69.0 | 71.4 |
| E2 SVM + noisy copies [recipe B] | 54.8 | 90.5 | 83.3 | 78.6 | 83.3 |
| E3 fine-tuned, database [recipe B] | 38.1 | 81.0 | 81.0 | 71.4 | 97.6 |
| E3 fine-tuned, head [recipe B] | 42.9 | 85.7 | 88.1 | 83.3 | 97.6 |
| E4 fine-tuned + noisy copies [recipe B] | 64.3 | 92.9 | 85.7 | 85.7 | 97.6 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| E0 frozen database [recipe B] | 50.8 | 53.2 | 50.8 | 50.0 | 81.0 |
| E0 CLIP zero-shot [recipe B] | 7.9 | 4.8 | 7.9 | 7.1 | 15.9 |
| E1 frozen + noisy copies [recipe B] | 81.7 | 91.3 | 81.7 | 83.3 | 87.3 |
| E2 SVM + noisy copies [recipe B] | 84.1 | 96.0 | 92.9 | 90.5 | 93.7 |
| E3 fine-tuned, database [recipe B] | 77.8 | 91.3 | 92.1 | 85.7 | 99.2 |
| E3 fine-tuned, head [recipe B] | 80.2 | 94.4 | 95.2 | 92.1 | 99.2 |
| E4 fine-tuned + noisy copies [recipe B] | 87.3 | 96.0 | 94.4 | 92.1 | 99.2 |

## Test recipe (7 diseases), same images: the usual tables

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E0 frozen database [test recipe] | 100.0 | 93.3 | 71.9 | 40.0 | 76.3 | 840 |
| E0 CLIP zero-shot [test recipe] | 25.7 | 15.2 | 8.6 | 3.8 | 13.3 | 840 |
| E1 frozen + noisy copies [test recipe] | 100.0 | 100.0 | 98.6 | 95.7 | 98.6 | 840 |
| E2 SVM + noisy copies [test recipe] | 99.5 | 99.5 | 98.6 | 97.1 | 98.7 | 840 |
| E3 fine-tuned, database [test recipe] | 100.0 | 100.0 | 99.5 | 92.4 | 98.0 | 840 |
| E3 fine-tuned, head [test recipe] | 100.0 | 100.0 | 99.5 | 94.3 | 98.5 | 840 |
| E4 fine-tuned + noisy copies [test recipe] | 100.0 | 100.0 | 99.0 | 96.7 | 98.9 | 840 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| E0 frozen database [test recipe] | 81.2 | 48.2 | 73.0 | 34.4 |
| E0 CLIP zero-shot [test recipe] | 9.1 | 3.5 | 16.2 | 4.0 |
| E1 frozen + noisy copies [test recipe] | 98.8 | 95.3 | 98.4 | 96.0 |
| E2 SVM + noisy copies [test recipe] | 99.4 | 97.6 | 98.2 | 96.8 |
| E3 fine-tuned, database [test recipe] | 98.5 | 94.1 | 97.6 | 91.2 |
| E3 fine-tuned, head [test recipe] | 97.9 | 91.8 | 98.8 | 96.0 |
| E4 fine-tuned + noisy copies [test recipe] | 98.8 | 96.5 | 99.0 | 96.8 |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| E0 frozen database [test recipe] | 26.2 | 33.3 | 28.6 | 54.8 | 57.1 |
| E0 CLIP zero-shot [test recipe] | 4.8 | 0.0 | 0.0 | 11.9 | 2.4 |
| E1 frozen + noisy copies [test recipe] | 85.7 | 100.0 | 97.6 | 100.0 | 95.2 |
| E2 SVM + noisy copies [test recipe] | 90.5 | 100.0 | 100.0 | 100.0 | 95.2 |
| E3 fine-tuned, database [test recipe] | 85.7 | 95.2 | 90.5 | 95.2 | 95.2 |
| E3 fine-tuned, head [test recipe] | 90.5 | 100.0 | 90.5 | 97.6 | 92.9 |
| E4 fine-tuned + noisy copies [test recipe] | 90.5 | 100.0 | 97.6 | 97.6 | 97.6 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| E0 frozen database [test recipe] | 61.1 | 70.6 | 61.9 | 70.6 | 77.8 |
| E0 CLIP zero-shot [test recipe] | 5.6 | 9.5 | 7.1 | 16.7 | 7.1 |
| E1 frozen + noisy copies [test recipe] | 95.2 | 99.2 | 98.4 | 99.2 | 98.4 |
| E2 SVM + noisy copies [test recipe] | 96.8 | 100.0 | 97.6 | 99.2 | 98.4 |
| E3 fine-tuned, database [test recipe] | 95.2 | 98.4 | 96.0 | 98.4 | 98.4 |
| E3 fine-tuned, head [test recipe] | 96.8 | 100.0 | 96.0 | 99.2 | 97.6 |
| E4 fine-tuned + noisy copies [test recipe] | 96.8 | 100.0 | 98.4 | 98.4 | 99.2 |

## Recipe B (black gram): the usual tables

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E0 frozen database [recipe B] | 100.0 | 46.7 | 23.3 | 0.0 | 42.5 | 120 |
| E0 CLIP zero-shot [recipe B] | 0.0 | 3.3 | 13.3 | 13.3 | 7.5 | 120 |
| E1 frozen + noisy copies [recipe B] | 100.0 | 93.3 | 80.0 | 20.0 | 73.3 | 120 |
| E2 SVM + noisy copies [recipe B] | 100.0 | 93.3 | 93.3 | 70.0 | 89.2 | 120 |
| E3 fine-tuned, database [recipe B] | 100.0 | 96.7 | 93.3 | 63.3 | 88.3 | 120 |
| E3 fine-tuned, head [recipe B] | 100.0 | 96.7 | 96.7 | 73.3 | 91.7 | 120 |
| E4 fine-tuned + noisy copies [recipe B] | 100.0 | 96.7 | 96.7 | 76.7 | 92.5 | 120 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| E0 frozen database [recipe B] | 42.5 | 0.0 | nan | nan |
| E0 CLIP zero-shot [recipe B] | 7.5 | 13.3 | nan | nan |
| E1 frozen + noisy copies [recipe B] | 73.3 | 20.0 | nan | nan |
| E2 SVM + noisy copies [recipe B] | 89.2 | 70.0 | nan | nan |
| E3 fine-tuned, database [recipe B] | 88.3 | 63.3 | nan | nan |
| E3 fine-tuned, head [recipe B] | 91.7 | 73.3 | nan | nan |
| E4 fine-tuned + noisy copies [recipe B] | 92.5 | 76.7 | nan | nan |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| E0 frozen database [recipe B] | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| E0 CLIP zero-shot [recipe B] | 16.7 | 0.0 | 16.7 | 33.3 | 0.0 |
| E1 frozen + noisy copies [recipe B] | 0.0 | 33.3 | 16.7 | 16.7 | 33.3 |
| E2 SVM + noisy copies [recipe B] | 50.0 | 66.7 | 50.0 | 83.3 | 100.0 |
| E3 fine-tuned, database [recipe B] | 33.3 | 100.0 | 33.3 | 66.7 | 83.3 |
| E3 fine-tuned, head [recipe B] | 33.3 | 100.0 | 66.7 | 83.3 | 83.3 |
| E4 fine-tuned + noisy copies [recipe B] | 66.7 | 100.0 | 66.7 | 50.0 | 100.0 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| E0 frozen database [recipe B] | 11.1 | 22.2 | 16.7 | 0.0 | 66.7 |
| E0 CLIP zero-shot [recipe B] | 16.7 | 0.0 | 22.2 | 11.1 | 0.0 |
| E1 frozen + noisy copies [recipe B] | 55.6 | 72.2 | 55.6 | 61.1 | 77.8 |
| E2 SVM + noisy copies [recipe B] | 83.3 | 88.9 | 77.8 | 77.8 | 100.0 |
| E3 fine-tuned, database [recipe B] | 61.1 | 100.0 | 77.8 | 88.9 | 94.4 |
| E3 fine-tuned, head [recipe B] | 66.7 | 100.0 | 88.9 | 94.4 | 94.4 |
| E4 fine-tuned + noisy copies [recipe B] | 77.8 | 100.0 | 88.9 | 83.3 | 100.0 |

## Test recipe (black gram), same images: the usual tables

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E0 frozen database [test recipe] | 100.0 | 66.7 | 20.0 | 6.7 | 48.3 | 120 |
| E0 CLIP zero-shot [test recipe] | 0.0 | 3.3 | 6.7 | 10.0 | 5.0 | 120 |
| E1 frozen + noisy copies [test recipe] | 100.0 | 96.7 | 86.7 | 90.0 | 93.3 | 120 |
| E2 SVM + noisy copies [test recipe] | 100.0 | 100.0 | 100.0 | 96.7 | 99.2 | 120 |
| E3 fine-tuned, database [test recipe] | 100.0 | 96.7 | 93.3 | 80.0 | 92.5 | 120 |
| E3 fine-tuned, head [test recipe] | 100.0 | 96.7 | 96.7 | 93.3 | 96.7 | 120 |
| E4 fine-tuned + noisy copies [test recipe] | 100.0 | 96.7 | 96.7 | 90.0 | 95.8 | 120 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| E0 frozen database [test recipe] | 48.3 | 6.7 | nan | nan |
| E0 CLIP zero-shot [test recipe] | 5.0 | 10.0 | nan | nan |
| E1 frozen + noisy copies [test recipe] | 93.3 | 90.0 | nan | nan |
| E2 SVM + noisy copies [test recipe] | 99.2 | 96.7 | nan | nan |
| E3 fine-tuned, database [test recipe] | 92.5 | 80.0 | nan | nan |
| E3 fine-tuned, head [test recipe] | 96.7 | 93.3 | nan | nan |
| E4 fine-tuned + noisy copies [test recipe] | 95.8 | 90.0 | nan | nan |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| E0 frozen database [test recipe] | 0.0 | 0.0 | 0.0 | 0.0 | 33.3 |
| E0 CLIP zero-shot [test recipe] | 16.7 | 0.0 | 0.0 | 0.0 | 33.3 |
| E1 frozen + noisy copies [test recipe] | 50.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| E2 SVM + noisy copies [test recipe] | 100.0 | 100.0 | 100.0 | 83.3 | 100.0 |
| E3 fine-tuned, database [test recipe] | 16.7 | 100.0 | 83.3 | 100.0 | 100.0 |
| E3 fine-tuned, head [test recipe] | 66.7 | 100.0 | 100.0 | 100.0 | 100.0 |
| E4 fine-tuned + noisy copies [test recipe] | 50.0 | 100.0 | 100.0 | 100.0 | 100.0 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| E0 frozen database [test recipe] | 27.8 | 22.2 | 27.8 | 0.0 | 77.8 |
| E0 CLIP zero-shot [test recipe] | 16.7 | 0.0 | 5.6 | 0.0 | 11.1 |
| E1 frozen + noisy copies [test recipe] | 72.2 | 94.4 | 94.4 | 94.4 | 100.0 |
| E2 SVM + noisy copies [test recipe] | 100.0 | 100.0 | 100.0 | 94.4 | 100.0 |
| E3 fine-tuned, database [test recipe] | 55.6 | 100.0 | 94.4 | 100.0 | 100.0 |
| E3 fine-tuned, head [test recipe] | 77.8 | 100.0 | 100.0 | 100.0 | 100.0 |
| E4 fine-tuned + noisy copies [test recipe] | 72.2 | 100.0 | 100.0 | 100.0 | 100.0 |

## Methods against each other on recipe B (7 diseases) (McNemar)

| Method A | Method B | Levels | Images | Only A right | Only B right | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E0 frozen database | E0 CLIP zero-shot | L3 | 210 | 64 | 3 | <0.001 |
| E0 frozen database | E0 CLIP zero-shot | All | 840 | 477 | 16 | <0.001 |
| E0 frozen database | E1 frozen + noisy copies | L3 | 210 | 9 | 86 | <0.001 |
| E0 frozen database | E1 frozen + noisy copies | All | 840 | 20 | 196 | <0.001 |
| E0 frozen database | E2 SVM + noisy copies | L3 | 210 | 4 | 104 | <0.001 |
| E0 frozen database | E2 SVM + noisy copies | All | 840 | 6 | 221 | <0.001 |
| E0 frozen database | E3 fine-tuned, database | L3 | 210 | 1 | 92 | <0.001 |
| E0 frozen database | E3 fine-tuned, database | All | 840 | 6 | 208 | <0.001 |
| E0 frozen database | E3 fine-tuned, head | L3 | 210 | 1 | 104 | <0.001 |
| E0 frozen database | E3 fine-tuned, head | All | 840 | 4 | 225 | <0.001 |
| E0 frozen database | E4 fine-tuned + noisy copies | L3 | 210 | 1 | 116 | <0.001 |
| E0 frozen database | E4 fine-tuned + noisy copies | All | 840 | 5 | 236 | <0.001 |
| E0 CLIP zero-shot | E1 frozen + noisy copies | L3 | 210 | 2 | 140 | <0.001 |
| E0 CLIP zero-shot | E1 frozen + noisy copies | All | 840 | 9 | 646 | <0.001 |
| E0 CLIP zero-shot | E2 SVM + noisy copies | L3 | 210 | 1 | 162 | <0.001 |
| E0 CLIP zero-shot | E2 SVM + noisy copies | All | 840 | 1 | 677 | <0.001 |
| E0 CLIP zero-shot | E3 fine-tuned, database | L3 | 210 | 2 | 154 | <0.001 |
| E0 CLIP zero-shot | E3 fine-tuned, database | All | 840 | 5 | 668 | <0.001 |
| E0 CLIP zero-shot | E3 fine-tuned, head | L3 | 210 | 1 | 165 | <0.001 |
| E0 CLIP zero-shot | E3 fine-tuned, head | All | 840 | 2 | 684 | <0.001 |
| E0 CLIP zero-shot | E4 fine-tuned + noisy copies | L3 | 210 | 2 | 178 | <0.001 |
| E0 CLIP zero-shot | E4 fine-tuned + noisy copies | All | 840 | 4 | 696 | <0.001 |
| E1 frozen + noisy copies | E2 SVM + noisy copies | L3 | 210 | 11 | 34 | <0.001 |
| E1 frozen + noisy copies | E2 SVM + noisy copies | All | 840 | 18 | 57 | <0.001 |
| E1 frozen + noisy copies | E3 fine-tuned, database | L3 | 210 | 20 | 34 | 0.076 |
| E1 frozen + noisy copies | E3 fine-tuned, database | All | 840 | 27 | 53 | 0.005 |
| E1 frozen + noisy copies | E3 fine-tuned, head | L3 | 210 | 16 | 42 | <0.001 |
| E1 frozen + noisy copies | E3 fine-tuned, head | All | 840 | 18 | 63 | <0.001 |
| E1 frozen + noisy copies | E4 fine-tuned + noisy copies | L3 | 210 | 6 | 44 | <0.001 |
| E1 frozen + noisy copies | E4 fine-tuned + noisy copies | All | 840 | 9 | 64 | <0.001 |
| E2 SVM + noisy copies | E3 fine-tuned, database | L3 | 210 | 27 | 18 | 0.233 |
| E2 SVM + noisy copies | E3 fine-tuned, database | All | 840 | 39 | 26 | 0.136 |
| E2 SVM + noisy copies | E3 fine-tuned, head | L3 | 210 | 18 | 21 | 0.749 |
| E2 SVM + noisy copies | E3 fine-tuned, head | All | 840 | 23 | 29 | 0.488 |
| E2 SVM + noisy copies | E4 fine-tuned + noisy copies | L3 | 210 | 13 | 28 | 0.028 |
| E2 SVM + noisy copies | E4 fine-tuned + noisy copies | All | 840 | 20 | 36 | 0.044 |
| E3 fine-tuned, database | E3 fine-tuned, head | L3 | 210 | 2 | 14 | 0.004 |
| E3 fine-tuned, database | E3 fine-tuned, head | All | 840 | 2 | 21 | <0.001 |
| E3 fine-tuned, database | E4 fine-tuned + noisy copies | L3 | 210 | 0 | 24 | <0.001 |
| E3 fine-tuned, database | E4 fine-tuned + noisy copies | All | 840 | 0 | 29 | <0.001 |
| E3 fine-tuned, head | E4 fine-tuned + noisy copies | L3 | 210 | 7 | 19 | 0.029 |
| E3 fine-tuned, head | E4 fine-tuned + noisy copies | All | 840 | 9 | 19 | 0.087 |

## Methods against each other on recipe B (black gram) (McNemar)

| Method A | Method B | Levels | Images | Only A right | Only B right | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E0 frozen database | E0 CLIP zero-shot | L3 | 30 | 0 | 4 | 0.125 |
| E0 frozen database | E0 CLIP zero-shot | All | 120 | 51 | 9 | <0.001 |
| E0 frozen database | E1 frozen + noisy copies | L3 | 30 | 0 | 6 | 0.031 |
| E0 frozen database | E1 frozen + noisy copies | All | 120 | 0 | 37 | <0.001 |
| E0 frozen database | E2 SVM + noisy copies | L3 | 30 | 0 | 21 | <0.001 |
| E0 frozen database | E2 SVM + noisy copies | All | 120 | 0 | 56 | <0.001 |
| E0 frozen database | E3 fine-tuned, database | L3 | 30 | 0 | 19 | <0.001 |
| E0 frozen database | E3 fine-tuned, database | All | 120 | 0 | 55 | <0.001 |
| E0 frozen database | E3 fine-tuned, head | L3 | 30 | 0 | 22 | <0.001 |
| E0 frozen database | E3 fine-tuned, head | All | 120 | 0 | 59 | <0.001 |
| E0 frozen database | E4 fine-tuned + noisy copies | L3 | 30 | 0 | 23 | <0.001 |
| E0 frozen database | E4 fine-tuned + noisy copies | All | 120 | 0 | 60 | <0.001 |
| E0 CLIP zero-shot | E1 frozen + noisy copies | L3 | 30 | 2 | 4 | 0.688 |
| E0 CLIP zero-shot | E1 frozen + noisy copies | All | 120 | 5 | 84 | <0.001 |
| E0 CLIP zero-shot | E2 SVM + noisy copies | L3 | 30 | 0 | 17 | <0.001 |
| E0 CLIP zero-shot | E2 SVM + noisy copies | All | 120 | 0 | 98 | <0.001 |
| E0 CLIP zero-shot | E3 fine-tuned, database | L3 | 30 | 1 | 16 | <0.001 |
| E0 CLIP zero-shot | E3 fine-tuned, database | All | 120 | 3 | 100 | <0.001 |
| E0 CLIP zero-shot | E3 fine-tuned, head | L3 | 30 | 0 | 18 | <0.001 |
| E0 CLIP zero-shot | E3 fine-tuned, head | All | 120 | 2 | 103 | <0.001 |
| E0 CLIP zero-shot | E4 fine-tuned + noisy copies | L3 | 30 | 0 | 19 | <0.001 |
| E0 CLIP zero-shot | E4 fine-tuned + noisy copies | All | 120 | 2 | 104 | <0.001 |
| E1 frozen + noisy copies | E2 SVM + noisy copies | L3 | 30 | 0 | 15 | <0.001 |
| E1 frozen + noisy copies | E2 SVM + noisy copies | All | 120 | 2 | 21 | <0.001 |
| E1 frozen + noisy copies | E3 fine-tuned, database | L3 | 30 | 1 | 14 | <0.001 |
| E1 frozen + noisy copies | E3 fine-tuned, database | All | 120 | 2 | 20 | <0.001 |
| E1 frozen + noisy copies | E3 fine-tuned, head | L3 | 30 | 0 | 16 | <0.001 |
| E1 frozen + noisy copies | E3 fine-tuned, head | All | 120 | 0 | 22 | <0.001 |
| E1 frozen + noisy copies | E4 fine-tuned + noisy copies | L3 | 30 | 0 | 17 | <0.001 |
| E1 frozen + noisy copies | E4 fine-tuned + noisy copies | All | 120 | 0 | 23 | <0.001 |
| E2 SVM + noisy copies | E3 fine-tuned, database | L3 | 30 | 6 | 4 | 0.754 |
| E2 SVM + noisy copies | E3 fine-tuned, database | All | 120 | 9 | 8 | 1.000 |
| E2 SVM + noisy copies | E3 fine-tuned, head | L3 | 30 | 3 | 4 | 1.000 |
| E2 SVM + noisy copies | E3 fine-tuned, head | All | 120 | 5 | 8 | 0.581 |
| E2 SVM + noisy copies | E4 fine-tuned + noisy copies | L3 | 30 | 4 | 6 | 0.754 |
| E2 SVM + noisy copies | E4 fine-tuned + noisy copies | All | 120 | 6 | 10 | 0.454 |
| E3 fine-tuned, database | E3 fine-tuned, head | L3 | 30 | 0 | 3 | 0.250 |
| E3 fine-tuned, database | E3 fine-tuned, head | All | 120 | 0 | 4 | 0.125 |
| E3 fine-tuned, database | E4 fine-tuned + noisy copies | L3 | 30 | 1 | 5 | 0.219 |
| E3 fine-tuned, database | E4 fine-tuned + noisy copies | All | 120 | 1 | 6 | 0.125 |
| E3 fine-tuned, head | E4 fine-tuned + noisy copies | L3 | 30 | 2 | 3 | 1.000 |
| E3 fine-tuned, head | E4 fine-tuned + noisy copies | All | 120 | 2 | 3 | 1.000 |
