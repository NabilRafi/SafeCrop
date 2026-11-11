# Recipe B calibration

Each knob is chosen so the average SSIM to the clean photo (grey values, 11 x 11 Gaussian window)
matches the test images' on the same 42 photos per noise type (calibration seeds 5005).
No model and no labels are used.

| Noise | Level | Knob | Value | SSIM test images | SSIM recipe B | Reachable |
| --- | --- | --- | --- | --- | --- | --- |
| Sensor noise | L1 | photons | 145.8 | 0.632 | 0.631 | yes |
| Sensor noise | L2 | photons | 29.15 | 0.332 | 0.333 | yes |
| Sensor noise | L3 | photons | 6.549 | 0.145 | 0.145 | yes |
| Hand-shake blur | L1 | path_px | 9.544 | 0.707 | 0.707 | yes |
| Hand-shake blur | L2 | path_px | 19.58 | 0.519 | 0.52 | yes |
| Hand-shake blur | L3 | path_px | 30.61 | 0.448 | 0.448 | yes |
| Out of focus | L1 | sigma_px | 1.853 | 0.692 | 0.691 | yes |
| Out of focus | L2 | sigma_px | 3.99 | 0.501 | 0.501 | yes |
| Out of focus | L3 | sigma_px | 7.316 | 0.419 | 0.419 | yes |
| Low light | L1 | light | 0.02046 | 0.516 | 0.516 | yes |
| Low light | L2 | light | 0.005298 | 0.304 | 0.304 | yes |
| Low light | L3 | light | 0.001779 | 0.168 | 0.169 | yes |
| Compression | L1 | badness | 0.457 | 0.847 | 0.847 | yes |
| Compression | L2 | badness | 0.7383 | 0.793 | 0.792 | yes |
| Compression | L3 | badness | 1.5 | 0.683 | 0.683 | yes |

Paste into src/safecrop/noise_b.py:

```python
PARAMS = {'gaussian_noise': {1: 145.8, 2: 29.15, 3: 6.549}, 'motion_blur': {1: 9.544, 2: 19.58, 3: 30.61}, 'defocus_blur': {1: 1.853, 2: 3.99, 3: 7.316}, 'low_light': {1: 0.02046, 2: 0.005298, 3: 0.001779}, 'jpeg_compression': {1: 0.457, 2: 0.7383, 3: 1.5}}
```
