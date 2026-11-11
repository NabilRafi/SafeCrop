# Recipe B test set

630 noisy images (seed family 4242) + the 210 original clean photos.
Average SSIM to the clean photo, test recipe vs recipe B (same photos):

| Noise | Level | SSIM test images | SSIM recipe B |
| --- | --- | --- | --- |
| Out of focus | L1 | 0.692 | 0.691 |
| Out of focus | L2 | 0.501 | 0.501 |
| Out of focus | L3 | 0.419 | 0.419 |
| Sensor noise | L1 | 0.632 | 0.632 |
| Sensor noise | L2 | 0.332 | 0.333 |
| Sensor noise | L3 | 0.145 | 0.145 |
| Compression | L1 | 0.847 | 0.847 |
| Compression | L2 | 0.793 | 0.792 |
| Compression | L3 | 0.683 | 0.683 |
| Low light | L1 | 0.516 | 0.516 |
| Low light | L2 | 0.304 | 0.304 |
| Low light | L3 | 0.168 | 0.168 |
| Hand-shake blur | L1 | 0.707 | 0.709 |
| Hand-shake blur | L2 | 0.52 | 0.532 |
| Hand-shake blur | L3 | 0.448 | 0.454 |

Wrote data/manifest_recipe_b.csv (840 rows).
