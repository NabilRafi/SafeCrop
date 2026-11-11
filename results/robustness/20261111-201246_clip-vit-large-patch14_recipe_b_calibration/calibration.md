# Recipe B calibration

Each knob is chosen so the average levelled colour SSIM to the clean photo (per RGB channel, brightness and contrast matched first)
matches the test images' on the same 42 photos per noise type (calibration seeds 5005).
No model and no labels are used.

| Noise | Level | Knob | Value | SSIM test images | SSIM recipe B | Reachable |
| --- | --- | --- | --- | --- | --- | --- |
| Sensor noise | L1 | photons | 91.35 | 0.496 | 0.496 | yes |
| Sensor noise | L2 | photons | 17.14 | 0.254 | 0.254 | yes |
| Sensor noise | L3 | photons | 3.473 | 0.127 | 0.127 | yes |
| Hand-shake blur | L1 | path_px | 9.544 | 0.705 | 0.705 | yes |
| Hand-shake blur | L2 | path_px | 19.64 | 0.507 | 0.507 | yes |
| Hand-shake blur | L3 | path_px | 31.31 | 0.425 | 0.425 | yes |
| Out of focus | L1 | sigma_px | 1.839 | 0.687 | 0.687 | yes |
| Out of focus | L2 | sigma_px | 3.98 | 0.484 | 0.484 | yes |
| Out of focus | L3 | sigma_px | 7.238 | 0.388 | 0.388 | yes |
| Low light | L1 | light | 0.02556 | 0.479 | 0.479 | yes |
| Low light | L2 | light | 0.0113 | 0.36 | 0.361 | yes |
| Low light | L3 | light | 0.005298 | 0.266 | 0.266 | yes |
| Compression | L1 | badness | 0.508 | 0.797 | 0.796 | yes |
| Compression | L2 | badness | 0.8324 | 0.737 | 0.736 | yes |
| Compression | L3 | badness | 1.57 | 0.62 | 0.623 | yes |

Paste into src/safecrop/noise_b.py:

```python
PARAMS = {'gaussian_noise': {1: 91.35, 2: 17.14, 3: 3.473}, 'motion_blur': {1: 9.544, 2: 19.64, 3: 31.31}, 'defocus_blur': {1: 1.839, 2: 3.98, 3: 7.238}, 'low_light': {1: 0.02556, 2: 0.0113, 3: 0.005298}, 'jpeg_compression': {1: 0.508, 2: 0.8324, 3: 1.57}}
```
