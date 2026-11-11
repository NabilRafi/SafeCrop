# Recipe B calibration

Each knob is chosen so the average levelled SSIM to the clean photo (grey values, brightness and contrast matched first)
matches the test images' on the same 42 photos per noise type (calibration seeds 5005).
No model and no labels are used.

| Noise | Level | Knob | Value | SSIM test images | SSIM recipe B | Reachable |
| --- | --- | --- | --- | --- | --- | --- |
| Sensor noise | L1 | photons | 143.9 | 0.641 | 0.641 | yes |
| Sensor noise | L2 | photons | 27.35 | 0.361 | 0.361 | yes |
| Sensor noise | L3 | photons | 5.697 | 0.183 | 0.183 | yes |
| Hand-shake blur | L1 | path_px | 9.632 | 0.71 | 0.71 | yes |
| Hand-shake blur | L2 | path_px | 19.46 | 0.519 | 0.519 | yes |
| Hand-shake blur | L3 | path_px | 30.61 | 0.44 | 0.44 | yes |
| Out of focus | L1 | sigma_px | 1.882 | 0.698 | 0.698 | yes |
| Out of focus | L2 | sigma_px | 4.087 | 0.502 | 0.503 | yes |
| Out of focus | L3 | sigma_px | 7.625 | 0.411 | 0.411 | yes |
| Low light | L1 | light | 0.02518 | 0.552 | 0.552 | yes |
| Low light | L2 | light | 0.009737 | 0.409 | 0.409 | yes |
| Low light | L3 | light | 0.004178 | 0.294 | 0.294 | yes |
| Compression | L1 | badness | 0.4683 | 0.847 | 0.846 | yes |
| Compression | L2 | badness | 0.7401 | 0.793 | 0.792 | yes |
| Compression | L3 | badness | 1.518 | 0.682 | 0.684 | yes |

Paste into src/safecrop/noise_b.py:

```python
PARAMS = {'gaussian_noise': {1: 143.9, 2: 27.35, 3: 5.697}, 'motion_blur': {1: 9.632, 2: 19.46, 3: 30.61}, 'defocus_blur': {1: 1.882, 2: 4.087, 3: 7.625}, 'low_light': {1: 0.02518, 2: 0.009737, 3: 0.004178}, 'jpeg_compression': {1: 0.4683, 2: 0.7401, 3: 1.518}}
```
