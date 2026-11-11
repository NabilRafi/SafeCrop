# Recipe B calibration

Each knob is chosen so the average levelled colour MS-SSIM to the clean photo (multi-scale, per RGB channel, brightness and contrast matched first)
matches the test images' on the same 42 photos per noise type (calibration seeds 5005).
No model and no labels are used.

| Noise | Level | Knob | Value | SSIM test images | SSIM recipe B | Reachable |
| --- | --- | --- | --- | --- | --- | --- |
| Sensor noise | L1 | photons | 241.3 | 0.89 | 0.891 | yes |
| Sensor noise | L2 | photons | 51.83 | 0.731 | 0.731 | yes |
| Sensor noise | L3 | photons | 10.98 | 0.514 | 0.514 | yes |
| Hand-shake blur | L1 | path_px | 13.45 | 0.885 | 0.885 | yes |
| Hand-shake blur | L2 | path_px | 30.02 | 0.702 | 0.702 | yes |
| Hand-shake blur | L3 | path_px | 50.21 | 0.571 | 0.57 | yes |
| Out of focus | L1 | sigma_px | 1.747 | 0.935 | 0.935 | yes |
| Out of focus | L2 | sigma_px | 3.68 | 0.817 | 0.817 | yes |
| Out of focus | L3 | sigma_px | 6.562 | 0.682 | 0.681 | yes |
| Low light | L1 | light | 0.08258 | 0.874 | 0.874 | yes |
| Low light | L2 | light | 0.03704 | 0.807 | 0.807 | yes |
| Low light | L3 | light | 0.01776 | 0.727 | 0.727 | yes |
| Compression | L1 | badness | 0.5625 | 0.95 | 0.95 | yes |
| Compression | L2 | badness | 0.9375 | 0.923 | 0.923 | yes |
| Compression | L3 | badness | 1.781 | 0.854 | 0.855 | yes |

Paste into src/safecrop/noise_b.py:

```python
PARAMS = {'gaussian_noise': {1: 241.3, 2: 51.83, 3: 10.98}, 'motion_blur': {1: 13.45, 2: 30.02, 3: 50.21}, 'defocus_blur': {1: 1.747, 2: 3.68, 3: 6.562}, 'low_light': {1: 0.08258, 2: 0.03704, 3: 0.01776}, 'jpeg_compression': {1: 0.5625, 2: 0.9375, 3: 1.781}}
```
