# 8 diseases (black gram added) on the original noise, 11 Nov

All runs: default settings, 5 folds by photo (black gram has its own folds, 6 photos each), 960 images.

## Old 840 images, 8 choices (comparable images; the methods could also answer black gram)

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E0 frozen database [8 diseases] | 100.0 | 93.3 | 71.9 | 40.0 | 76.3 | 840 |
| E0 CLIP zero-shot (33 options) [8 diseases] | 25.7 | 15.2 | 8.6 | 3.8 | 13.3 | 840 |
| E1 frozen + noisy copies [8 diseases] | 100.0 | 100.0 | 98.6 | 95.7 | 98.6 | 840 |
| E2 SVM + noisy copies [8 diseases] | 99.5 | 99.5 | 98.6 | 97.1 | 98.7 | 840 |
| E3 fine-tuned, database [8 diseases] | 100.0 | 100.0 | 99.5 | 92.4 | 98.0 | 840 |
| E3 fine-tuned, head [8 diseases] | 100.0 | 100.0 | 99.5 | 94.3 | 98.5 | 840 |
| E4 fine-tuned + noisy copies [8 diseases] | 100.0 | 100.0 | 99.0 | 96.7 | 98.9 | 840 |
| CLIP database, frozen (Step 2) | 100.0 | 93.3 | 71.9 | 40.0 | 76.3 | 840 |
| Gemini + references + descriptions (Step 2b) | 100.0 | 92.9 | 75.2 | 47.1 | 78.8 | 840 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| E0 frozen database [8 diseases] | 81.2 | 48.2 | 73.0 | 34.4 |
| E0 CLIP zero-shot (33 options) [8 diseases] | 9.1 | 3.5 | 16.2 | 4.0 |
| E1 frozen + noisy copies [8 diseases] | 98.8 | 95.3 | 98.4 | 96.0 |
| E2 SVM + noisy copies [8 diseases] | 99.4 | 97.6 | 98.2 | 96.8 |
| E3 fine-tuned, database [8 diseases] | 98.5 | 94.1 | 97.6 | 91.2 |
| E3 fine-tuned, head [8 diseases] | 97.9 | 91.8 | 98.8 | 96.0 |
| E4 fine-tuned + noisy copies [8 diseases] | 98.8 | 96.5 | 99.0 | 96.8 |
| CLIP database, frozen (Step 2) | 81.2 | 48.2 | 73.0 | 34.4 |
| Gemini + references + descriptions (Step 2b) | 80.6 | 48.2 | 77.6 | 46.4 |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| E0 frozen database [8 diseases] | 26.2 | 33.3 | 28.6 | 54.8 | 57.1 |
| E0 CLIP zero-shot (33 options) [8 diseases] | 4.8 | 0.0 | 0.0 | 11.9 | 2.4 |
| E1 frozen + noisy copies [8 diseases] | 85.7 | 100.0 | 97.6 | 100.0 | 95.2 |
| E2 SVM + noisy copies [8 diseases] | 90.5 | 100.0 | 100.0 | 100.0 | 95.2 |
| E3 fine-tuned, database [8 diseases] | 85.7 | 95.2 | 90.5 | 95.2 | 95.2 |
| E3 fine-tuned, head [8 diseases] | 90.5 | 100.0 | 90.5 | 97.6 | 92.9 |
| E4 fine-tuned + noisy copies [8 diseases] | 90.5 | 100.0 | 97.6 | 97.6 | 97.6 |
| CLIP database, frozen (Step 2) | 26.2 | 33.3 | 28.6 | 54.8 | 57.1 |
| Gemini + references + descriptions (Step 2b) | 31.0 | 52.4 | 38.1 | 52.4 | 61.9 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| E0 frozen database [8 diseases] | 61.1 | 70.6 | 61.9 | 70.6 | 77.8 |
| E0 CLIP zero-shot (33 options) [8 diseases] | 5.6 | 9.5 | 7.1 | 16.7 | 7.1 |
| E1 frozen + noisy copies [8 diseases] | 95.2 | 99.2 | 98.4 | 99.2 | 98.4 |
| E2 SVM + noisy copies [8 diseases] | 96.8 | 100.0 | 97.6 | 99.2 | 98.4 |
| E3 fine-tuned, database [8 diseases] | 95.2 | 98.4 | 96.0 | 98.4 | 98.4 |
| E3 fine-tuned, head [8 diseases] | 96.8 | 100.0 | 96.0 | 99.2 | 97.6 |
| E4 fine-tuned + noisy copies [8 diseases] | 96.8 | 100.0 | 98.4 | 98.4 | 99.2 |
| CLIP database, frozen (Step 2) | 61.1 | 70.6 | 61.9 | 70.6 | 77.8 |
| Gemini + references + descriptions (Step 2b) | 61.1 | 78.6 | 65.9 | 69.0 | 84.1 |

### Head to head (McNemar exact test)

| New | Baseline | Levels | Images | Only new right | Only baseline right | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E0 frozen database [8 diseases] | CLIP database, frozen (Step 2) | All | 840 | 0 | 0 | 1.000 |
| E0 frozen database [8 diseases] | CLIP database, frozen (Step 2) | L3 | 210 | 0 | 0 | 1.000 |
| E0 frozen database [8 diseases] | Gemini + references + descriptions (Step 2b) | All | 840 | 12 | 33 | 0.002 |
| E0 frozen database [8 diseases] | Gemini + references + descriptions (Step 2b) | L3 | 210 | 3 | 18 | 0.001 |
| E0 CLIP zero-shot (33 options) [8 diseases] | CLIP database, frozen (Step 2) | All | 840 | 15 | 544 | <0.001 |
| E0 CLIP zero-shot (33 options) [8 diseases] | CLIP database, frozen (Step 2) | L3 | 210 | 7 | 83 | <0.001 |
| E0 CLIP zero-shot (33 options) [8 diseases] | Gemini + references + descriptions (Step 2b) | All | 840 | 17 | 567 | <0.001 |
| E0 CLIP zero-shot (33 options) [8 diseases] | Gemini + references + descriptions (Step 2b) | L3 | 210 | 7 | 98 | <0.001 |
| E1 frozen + noisy copies [8 diseases] | CLIP database, frozen (Step 2) | All | 840 | 193 | 6 | <0.001 |
| E1 frozen + noisy copies [8 diseases] | CLIP database, frozen (Step 2) | L3 | 210 | 121 | 4 | <0.001 |
| E1 frozen + noisy copies [8 diseases] | Gemini + references + descriptions (Step 2b) | All | 840 | 173 | 7 | <0.001 |
| E1 frozen + noisy copies [8 diseases] | Gemini + references + descriptions (Step 2b) | L3 | 210 | 107 | 5 | <0.001 |
| E2 SVM + noisy copies [8 diseases] | CLIP database, frozen (Step 2) | All | 840 | 192 | 4 | <0.001 |
| E2 SVM + noisy copies [8 diseases] | CLIP database, frozen (Step 2) | L3 | 210 | 122 | 2 | <0.001 |
| E2 SVM + noisy copies [8 diseases] | Gemini + references + descriptions (Step 2b) | All | 840 | 171 | 4 | <0.001 |
| E2 SVM + noisy copies [8 diseases] | Gemini + references + descriptions (Step 2b) | L3 | 210 | 107 | 2 | <0.001 |
| E3 fine-tuned, database [8 diseases] | CLIP database, frozen (Step 2) | All | 840 | 183 | 1 | <0.001 |
| E3 fine-tuned, database [8 diseases] | CLIP database, frozen (Step 2) | L3 | 210 | 111 | 1 | <0.001 |
| E3 fine-tuned, database [8 diseases] | Gemini + references + descriptions (Step 2b) | All | 840 | 163 | 2 | <0.001 |
| E3 fine-tuned, database [8 diseases] | Gemini + references + descriptions (Step 2b) | L3 | 210 | 97 | 2 | <0.001 |
| E3 fine-tuned, head [8 diseases] | CLIP database, frozen (Step 2) | All | 840 | 187 | 1 | <0.001 |
| E3 fine-tuned, head [8 diseases] | CLIP database, frozen (Step 2) | L3 | 210 | 115 | 1 | <0.001 |
| E3 fine-tuned, head [8 diseases] | Gemini + references + descriptions (Step 2b) | All | 840 | 166 | 1 | <0.001 |
| E3 fine-tuned, head [8 diseases] | Gemini + references + descriptions (Step 2b) | L3 | 210 | 100 | 1 | <0.001 |
| E4 fine-tuned + noisy copies [8 diseases] | CLIP database, frozen (Step 2) | All | 840 | 191 | 1 | <0.001 |
| E4 fine-tuned + noisy copies [8 diseases] | CLIP database, frozen (Step 2) | L3 | 210 | 120 | 1 | <0.001 |
| E4 fine-tuned + noisy copies [8 diseases] | Gemini + references + descriptions (Step 2b) | All | 840 | 171 | 2 | <0.001 |
| E4 fine-tuned + noisy copies [8 diseases] | Gemini + references + descriptions (Step 2b) | L3 | 210 | 105 | 1 | <0.001 |

## Black gram yellow mosaic only (30 photos, 120 images)

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E0 frozen database | 100.0 | 66.7 | 20.0 | 6.7 | 48.3 | 120 |
| E0 CLIP zero-shot (33 options) | 0.0 | 3.3 | 6.7 | 10.0 | 5.0 | 120 |
| E1 frozen + noisy copies | 100.0 | 96.7 | 86.7 | 90.0 | 93.3 | 120 |
| E2 SVM + noisy copies | 100.0 | 100.0 | 100.0 | 96.7 | 99.2 | 120 |
| E3 fine-tuned, database | 100.0 | 96.7 | 93.3 | 80.0 | 92.5 | 120 |
| E3 fine-tuned, head | 100.0 | 96.7 | 96.7 | 93.3 | 96.7 | 120 |
| E4 fine-tuned + noisy copies | 100.0 | 96.7 | 96.7 | 90.0 | 95.8 | 120 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| E0 frozen database | 48.3 | 6.7 | nan | nan |
| E0 CLIP zero-shot (33 options) | 5.0 | 10.0 | nan | nan |
| E1 frozen + noisy copies | 93.3 | 90.0 | nan | nan |
| E2 SVM + noisy copies | 99.2 | 96.7 | nan | nan |
| E3 fine-tuned, database | 92.5 | 80.0 | nan | nan |
| E3 fine-tuned, head | 96.7 | 93.3 | nan | nan |
| E4 fine-tuned + noisy copies | 95.8 | 90.0 | nan | nan |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| E0 frozen database | 0.0 | 0.0 | 0.0 | 0.0 | 33.3 |
| E0 CLIP zero-shot (33 options) | 16.7 | 0.0 | 0.0 | 0.0 | 33.3 |
| E1 frozen + noisy copies | 50.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| E2 SVM + noisy copies | 100.0 | 100.0 | 100.0 | 83.3 | 100.0 |
| E3 fine-tuned, database | 16.7 | 100.0 | 83.3 | 100.0 | 100.0 |
| E3 fine-tuned, head | 66.7 | 100.0 | 100.0 | 100.0 | 100.0 |
| E4 fine-tuned + noisy copies | 50.0 | 100.0 | 100.0 | 100.0 | 100.0 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| E0 frozen database | 27.8 | 22.2 | 27.8 | 0.0 | 77.8 |
| E0 CLIP zero-shot (33 options) | 16.7 | 0.0 | 5.6 | 0.0 | 11.1 |
| E1 frozen + noisy copies | 72.2 | 94.4 | 94.4 | 94.4 | 100.0 |
| E2 SVM + noisy copies | 100.0 | 100.0 | 100.0 | 94.4 | 100.0 |
| E3 fine-tuned, database | 55.6 | 100.0 | 94.4 | 100.0 | 100.0 |
| E3 fine-tuned, head | 77.8 | 100.0 | 100.0 | 100.0 | 100.0 |
| E4 fine-tuned + noisy copies | 72.2 | 100.0 | 100.0 | 100.0 | 100.0 |

## Did adding black gram as an 8th choice change the old 840 images? (McNemar, same images)

| Method | Levels | 7 diseases % | 8 diseases % | Change | Only 8 right | Only 7 right | p | Old images called black gram |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| E0 frozen database | L3 | 40.0 | 40.0 | 0.0 | 0 | 0 | 1.000 |  |
| E0 frozen database | All | 76.3 | 76.3 | 0.0 | 0 | 0 | 1.000 | 0 |
| E0 CLIP zero-shot (33 options) | L3 | 3.8 | 3.8 | 0.0 | 0 | 0 | 1.000 |  |
| E0 CLIP zero-shot (33 options) | All | 13.3 | 13.3 | 0.0 | 0 | 0 | 1.000 | 14 |
| E1 frozen + noisy copies | L3 | 95.2 | 95.7 | 0.5 | 1 | 0 | 1.000 |  |
| E1 frozen + noisy copies | All | 98.6 | 98.6 | 0.0 | 1 | 1 | 1.000 | 4 |
| E2 SVM + noisy copies | L3 | 97.6 | 97.1 | -0.5 | 0 | 1 | 1.000 |  |
| E2 SVM + noisy copies | All | 99.0 | 98.7 | -0.3 | 0 | 3 | 0.250 | 4 |
| E3 fine-tuned, database | L3 | 93.8 | 92.4 | -1.4 | 0 | 3 | 0.250 |  |
| E3 fine-tuned, database | All | 98.3 | 98.0 | -0.3 | 0 | 3 | 0.250 | 0 |
| E3 fine-tuned, head | L3 | 95.2 | 94.3 | -0.9 | 1 | 3 | 0.625 |  |
| E3 fine-tuned, head | All | 98.7 | 98.5 | -0.2 | 1 | 3 | 0.625 | 2 |
| E4 fine-tuned + noisy copies | L3 | 97.1 | 96.7 | -0.4 | 0 | 1 | 1.000 |  |
| E4 fine-tuned + noisy copies | All | 99.2 | 98.9 | -0.3 | 0 | 2 | 0.500 | 0 |

## Mistakes involving black gram (all levels)

| Method | Black gram wrong (of 120) | Black gram called (top 3) | Old images called black gram (by true disease) |
| --- | ---: | ---: | ---: |
| E0 frozen database | 62 | jute_mosaic 26; rice_stem_borer 23; apple_scab 8 | - |
| E0 CLIP zero-shot (33 options) | 114 | apple_alternaria_leaf_spot 64; pear_leaf_spot 12; jute_healthy 10 | jute_dieback 5; jute_mosaic 5; pear_leaf_spot 3 |
| E1 frozen + noisy copies | 8 | jute_mosaic 3; jute_dieback 2; pear_leaf_spot 2 | jute_mosaic 2; jute_dieback 1; pear_leaf_spot 1 |
| E2 SVM + noisy copies | 1 | jute_dieback 1 | jute_dieback 2; rice_stem_borer 1; pear_leaf_spot 1 |
| E3 fine-tuned, database | 9 | jute_mosaic 6; grape_leaf_blight 1; apple_scab 1 | - |
| E3 fine-tuned, head | 4 | jute_mosaic 4 | apple_scab 1; jute_dieback 1 |
| E4 fine-tuned + noisy copies | 5 | jute_mosaic 3; pear_leaf_spot 1; jute_dieback 1 | - |
