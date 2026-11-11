# Recipe B test set

630 noisy images (seed family 4242) + the 210 original clean photos.
Average levelled SSIM to the clean photo (brightness and contrast matched first), test recipe vs recipe B:

| Noise | Level | SSIM test images | SSIM recipe B |
| --- | --- | --- | --- |
| Out of focus | L1 | 0.698 | 0.698 |
| Out of focus | L2 | 0.502 | 0.503 |
| Out of focus | L3 | 0.411 | 0.411 |
| Sensor noise | L1 | 0.641 | 0.641 |
| Sensor noise | L2 | 0.361 | 0.361 |
| Sensor noise | L3 | 0.183 | 0.183 |
| Compression | L1 | 0.847 | 0.848 |
| Compression | L2 | 0.793 | 0.792 |
| Compression | L3 | 0.682 | 0.684 |
| Low light | L1 | 0.552 | 0.551 |
| Low light | L2 | 0.409 | 0.411 |
| Low light | L3 | 0.294 | 0.294 |
| Hand-shake blur | L1 | 0.71 | 0.711 |
| Hand-shake blur | L2 | 0.519 | 0.534 |
| Hand-shake blur | L3 | 0.44 | 0.446 |

Wrote data/manifest_recipe_b.csv (840 rows).
