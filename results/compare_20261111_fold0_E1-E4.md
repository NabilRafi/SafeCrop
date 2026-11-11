# Fold-0 comparison: E1 vs E2 (SVM) vs E3 / E4 (fine-tuned), default settings

Images compared: 168 of 840 (folds [0]; all predictors scored them without seeing their photo).
E1 and E2 were run on all 840 images; here they are cut to the same fold-0 images.

### Accuracy by noise level (% correct)

| Predictor | L0 | L1 | L2 | L3 | All | n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E1 frozen + noisy copies (database) | 100.0 | 100.0 | 100.0 | 95.2 | 98.8 | 168 |
| E2 SVM, frozen + noisy copies | 100.0 | 97.6 | 97.6 | 97.6 | 98.2 | 168 |
| E3 fine-tuned (database) | 100.0 | 100.0 | 100.0 | 88.1 | 97.0 | 168 |
| E3 fine-tuned (head) | 100.0 | 100.0 | 100.0 | 95.2 | 98.8 | 168 |
| E4 fine-tuned + noisy copies (database) | 100.0 | 100.0 | 100.0 | 97.6 | 99.4 | 168 |
| CLIP database, frozen (Step 2) | 100.0 | 92.9 | 76.2 | 35.7 | 76.2 | 168 |
| Gemini + references + descriptions (Step 2b) | 100.0 | 92.9 | 81.0 | 40.5 | 78.6 | 168 |
| Gemini plain, 33 options (Step 2) | 64.3 | 42.9 | 16.7 | 9.5 | 33.3 | 168 |
| CLIP zero-shot, 33 options (Step 2) | 31.0 | 16.7 | 7.1 | 7.1 | 15.5 | 168 |

### Info-rich (A) vs info-scarce (B) (% correct)

| Predictor | A all | A L3 | B all | B L3 |
| --- | ---: | ---: | ---: | ---: |
| E1 frozen + noisy copies (database) | 98.5 | 94.1 | 99.0 | 96.0 |
| E2 SVM, frozen + noisy copies | 100.0 | 100.0 | 97.0 | 96.0 |
| E3 fine-tuned (database) | 98.5 | 94.1 | 96.0 | 84.0 |
| E3 fine-tuned (head) | 98.5 | 94.1 | 99.0 | 96.0 |
| E4 fine-tuned + noisy copies (database) | 100.0 | 100.0 | 99.0 | 96.0 |
| CLIP database, frozen (Step 2) | 82.4 | 47.1 | 72.0 | 28.0 |
| Gemini + references + descriptions (Step 2b) | 79.4 | 41.2 | 78.0 | 40.0 |
| Gemini plain, 33 options (Step 2) | 48.5 | 23.5 | 23.0 | 0.0 |
| CLIP zero-shot, 33 options (Step 2) | 10.3 | 5.9 | 19.0 | 8.0 |

### By noise type, L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| E1 frozen + noisy copies (database) | 90.0 | 100.0 | 100.0 | 100.0 | 87.5 |
| E2 SVM, frozen + noisy copies | 100.0 | 100.0 | 100.0 | 100.0 | 87.5 |
| E3 fine-tuned (database) | 90.0 | 87.5 | 75.0 | 100.0 | 87.5 |
| E3 fine-tuned (head) | 100.0 | 100.0 | 87.5 | 100.0 | 87.5 |
| E4 fine-tuned + noisy copies (database) | 100.0 | 100.0 | 100.0 | 100.0 | 87.5 |
| CLIP database, frozen (Step 2) | 40.0 | 25.0 | 25.0 | 50.0 | 37.5 |
| Gemini + references + descriptions (Step 2b) | 40.0 | 50.0 | 25.0 | 50.0 | 37.5 |
| Gemini plain, 33 options (Step 2) | 20.0 | 12.5 | 0.0 | 0.0 | 12.5 |
| CLIP zero-shot, 33 options (Step 2) | 10.0 | 0.0 | 0.0 | 25.0 | 0.0 |

### By noise type, L1-L3 (% correct)

| Predictor | Sensor noise | Hand-shake blur | Out of focus | Low light | Compression |
| --- | ---: | ---: | ---: | ---: | ---: |
| E1 frozen + noisy copies (database) | 96.7 | 100.0 | 100.0 | 100.0 | 95.8 |
| E2 SVM, frozen + noisy copies | 100.0 | 100.0 | 91.7 | 100.0 | 95.8 |
| E3 fine-tuned (database) | 96.7 | 95.8 | 91.7 | 100.0 | 95.8 |
| E3 fine-tuned (head) | 100.0 | 100.0 | 95.8 | 100.0 | 95.8 |
| E4 fine-tuned + noisy copies (database) | 100.0 | 100.0 | 100.0 | 100.0 | 95.8 |
| CLIP database, frozen (Step 2) | 66.7 | 75.0 | 58.3 | 75.0 | 66.7 |
| Gemini + references + descriptions (Step 2b) | 66.7 | 83.3 | 62.5 | 70.8 | 75.0 |
| Gemini plain, 33 options (Step 2) | 30.0 | 20.8 | 16.7 | 20.8 | 25.0 |
| CLIP zero-shot, 33 options (Step 2) | 10.0 | 16.7 | 0.0 | 20.8 | 4.2 |

## Fine-tuned vs E1 (frozen + noisy copies)

### Head to head (McNemar exact test)

| New | Baseline | Levels | Images | Only new right | Only baseline right | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E3 fine-tuned (database) | E1 frozen + noisy copies (database) | All | 168 | 1 | 4 | 0.375 |
| E3 fine-tuned (database) | E1 frozen + noisy copies (database) | L3 | 42 | 1 | 4 | 0.375 |
| E3 fine-tuned (head) | E1 frozen + noisy copies (database) | All | 168 | 1 | 1 | 1.000 |
| E3 fine-tuned (head) | E1 frozen + noisy copies (database) | L3 | 42 | 1 | 1 | 1.000 |
| E4 fine-tuned + noisy copies (database) | E1 frozen + noisy copies (database) | All | 168 | 1 | 0 | 1.000 |
| E4 fine-tuned + noisy copies (database) | E1 frozen + noisy copies (database) | L3 | 42 | 1 | 0 | 1.000 |

## Fine-tuned vs E2 (SVM)

### Head to head (McNemar exact test)

| New | Baseline | Levels | Images | Only new right | Only baseline right | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E3 fine-tuned (database) | E2 SVM, frozen + noisy copies | All | 168 | 2 | 4 | 0.688 |
| E3 fine-tuned (database) | E2 SVM, frozen + noisy copies | L3 | 42 | 0 | 4 | 0.125 |
| E3 fine-tuned (head) | E2 SVM, frozen + noisy copies | All | 168 | 2 | 1 | 1.000 |
| E3 fine-tuned (head) | E2 SVM, frozen + noisy copies | L3 | 42 | 0 | 1 | 1.000 |
| E4 fine-tuned + noisy copies (database) | E2 SVM, frozen + noisy copies | All | 168 | 2 | 0 | 0.500 |
| E4 fine-tuned + noisy copies (database) | E2 SVM, frozen + noisy copies | L3 | 42 | 0 | 0 | 1.000 |

## E2 (SVM) vs E1

### Head to head (McNemar exact test)

| New | Baseline | Levels | Images | Only new right | Only baseline right | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E2 SVM, frozen + noisy copies | E1 frozen + noisy copies (database) | All | 168 | 1 | 2 | 1.000 |
| E2 SVM, frozen + noisy copies | E1 frozen + noisy copies (database) | L3 | 42 | 1 | 0 | 1.000 |

## Fold-0 L3 images still wrong

| Predictor | Image | True | Predicted | Noise |
| --- | --- | --- | --- | --- |
| E1 frozen + noisy copies (database) | L3/jute_dieback/jute_dieback_026_jpeg_compression_L3.png | jute_dieback | apple_scab | jpeg_compression |
| E1 frozen + noisy copies (database) | L3/rice_stem_borer/rice_stem_borer_012_gaussian_noise_L3.png | rice_stem_borer | jute_dieback | gaussian_noise |
| E2 SVM, frozen + noisy copies | L3/jute_dieback/jute_dieback_026_jpeg_compression_L3.png | jute_dieback | jute_mosaic | jpeg_compression |
| E3 fine-tuned (database) | L3/apple_scab/apple_scab_012_defocus_blur_L3.png | apple_scab | jute_dieback | defocus_blur |
| E3 fine-tuned (database) | L3/grape_leaf_blight/grape_leaf_blight_028_motion_blur_L3.png | grape_leaf_blight | potato_late_blight | motion_blur |
| E3 fine-tuned (database) | L3/jute_dieback/jute_dieback_026_jpeg_compression_L3.png | jute_dieback | jute_mosaic | jpeg_compression |
| E3 fine-tuned (database) | L3/pear_leaf_spot/pear_leaf_spot_021_defocus_blur_L3.png | pear_leaf_spot | jute_mosaic | defocus_blur |
| E3 fine-tuned (database) | L3/pear_leaf_spot/pear_leaf_spot_027_gaussian_noise_L3.png | pear_leaf_spot | jute_mosaic | gaussian_noise |
| E3 fine-tuned (head) | L3/apple_scab/apple_scab_012_defocus_blur_L3.png | apple_scab | jute_dieback | defocus_blur |
| E3 fine-tuned (head) | L3/jute_dieback/jute_dieback_026_jpeg_compression_L3.png | jute_dieback | jute_mosaic | jpeg_compression |
| E4 fine-tuned + noisy copies (database) | L3/jute_dieback/jute_dieback_026_jpeg_compression_L3.png | jute_dieback | jute_mosaic | jpeg_compression |
