# Recipe B test set

720 noisy images (seed family 4242) + the 240 original clean photos (8 diseases).
Average levelled colour MS-SSIM to the clean photo (multi-scale, per RGB channel, brightness and contrast matched first), test recipe vs recipe B:

| Noise | Level | SSIM test images | SSIM recipe B |
| --- | --- | --- | --- |
| Out of focus | L1 | 0.938 | 0.937 |
| Out of focus | L2 | 0.819 | 0.818 |
| Out of focus | L3 | 0.679 | 0.679 |
| Sensor noise | L1 | 0.893 | 0.894 |
| Sensor noise | L2 | 0.735 | 0.738 |
| Sensor noise | L3 | 0.517 | 0.52 |
| Compression | L1 | 0.949 | 0.95 |
| Compression | L2 | 0.923 | 0.923 |
| Compression | L3 | 0.855 | 0.855 |
| Low light | L1 | 0.879 | 0.881 |
| Low light | L2 | 0.813 | 0.817 |
| Low light | L3 | 0.732 | 0.738 |
| Hand-shake blur | L1 | 0.885 | 0.885 |
| Hand-shake blur | L2 | 0.698 | 0.71 |
| Hand-shake blur | L3 | 0.566 | 0.572 |

Compared with data/manifest_recipe_b.csv: 873 of 960 images identical (960 matched by name).
Some images differ (usually a different WebP/OpenCV version); the CLIP scores use the images built here.
