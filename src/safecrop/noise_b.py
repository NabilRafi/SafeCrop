"""Recipe B: the same five noise types, made a DIFFERENT way (the robustness test).

Every method that learned from noisy copies (E1-E4) saw copies made with the test set's own recipe
(noise.py). Recipe B asks whether they still work when the noise is made differently, as it will be in
real phone photos. The 210 clean photos, their noise types and their folds stay the same; only the noisy
images (L1-L3) change. ``scripts/make_recipe_b.py`` builds them into data/images_recipe_b/.

How recipe B differs from the test recipe (noise.py):

  sensor noise     test: even Gaussian grain, separate for every pixel and colour
                   B:    grain that grows with brightness (photon shot noise), spread over neighbouring
                         pixels, plus colour blotches (what a phone's processing does to sensor noise)
  hand-shake blur  test: a straight line at -45..45 degrees, weights fading along the line
                   B:    a curved shake path in any direction, even weights along the path
  out of focus     test: a sharp-edged disk
                   B:    a smooth Gaussian blur plus colour fringes (red and blue shifted apart)
  low light        test: darker, grainy, faded colours, brightened only part of the way
                   B:    auto exposure brightens a very noisy dark photo all the way back, the phone
                         smooths the grain (and the detail), warm street-light colour cast
  compression      test: JPEG at quality 25 / 15 / 7
                   B:    messaging-app path: shrink, WebP, enlarge back

Severity: each noise type has one strength knob. ``make_recipe_b.py --calibrate`` picks it so the
average levelled colour SSIM (structural similarity to the clean photo on each colour channel, after
matching each channel's overall brightness and contrast, see ``ssim``) equals the test set's at each level,
on the same photos. No model and no labels are used to choose it.
"""
from __future__ import annotations

import io

import cv2
import numpy as np
from PIL import Image

from .noise import NOISE_TYPES, TEST_SEED

RECIPE_B_SEED = 4242        # seed family of the recipe-B test images (299 = test set, 2026 = noisy copies)
CALIBRATION_SEED = 5005     # seed family used only while choosing the knobs
assert len({RECIPE_B_SEED, CALIBRATION_SEED, TEST_SEED, 2026}) == 4

# name, lowest, highest, does SSIM go UP when the knob goes up?, search on a log scale?
KNOBS = {
    "gaussian_noise":   ("photons", 0.5, 5000.0, True, True),     # fewer photons -> more grain
    "motion_blur":      ("path_px", 0.5, 120.0, False, False),    # longer shake path -> more blur
    "defocus_blur":     ("sigma_px", 0.2, 20.0, False, False),    # wider blur
    "low_light":        ("light", 0.0005, 1.0, True, True),       # share of the light that reaches the camera
    "jpeg_compression": ("badness", 0.0, 3.0, False, False),      # smaller picture + lower WebP quality
}

# The knob of each noise type at L1 / L2 / L3, from `python scripts/make_recipe_b.py --calibrate`
# (11 Nov 2026, levelled colour MS-SSIM; every level matches the test images' average to within 0.001; table in
# results/robustness/20261111-202329_*_recipe_b_calibration/calibration.md). Do not change after scoring started.
PARAMS: dict[str, dict[int, float]] | None = {
    "gaussian_noise": {1: 241.3, 2: 51.83, 3: 10.98},      # photons
    "motion_blur": {1: 13.45, 2: 30.02, 3: 50.21},         # shake path length, px
    "defocus_blur": {1: 1.747, 2: 3.68, 3: 6.562},         # Gaussian blur sigma, px
    "low_light": {1: 0.08258, 2: 0.03704, 3: 0.01776},     # share of the light
    "jpeg_compression": {1: 0.5625, 2: 0.9375, 3: 1.781},  # badness (L3: 53% size, WebP quality 9)
}


# ----------------------------------------------------------------------------- helpers
def _f(img: np.ndarray) -> np.ndarray:
    return img.astype(np.float32) / 255.0


def _u8(x: np.ndarray) -> np.ndarray:
    return (np.clip(x, 0.0, 1.0) * 255.0 + 0.5).astype(np.uint8)


def _unit_noise(shape, blur_sigma: float) -> np.ndarray:
    """Gaussian noise spread over neighbouring pixels, scaled back to standard deviation 1."""
    n = cv2.GaussianBlur(np.random.normal(size=shape).astype(np.float32), (0, 0), blur_sigma)
    return n / (n.std() + 1e-8)


# ----------------------------------------------------------------------------- the five recipe-B effects
def sensor_noise_b(img: np.ndarray, photons: float) -> np.ndarray:
    x = _f(img)
    shot = np.random.poisson(x * photons) / photons               # grain grows with brightness
    h, w = x.shape[:2]
    s = 1.0 / np.sqrt(photons)
    grain = 0.5 * s * _unit_noise((h, w), 0.8)[..., None]         # clumped grey grain
    blotches = 0.35 * s * _unit_noise((h, w, 3), 2.5)             # colour blotches
    return _u8(shot + grain + blotches)


def shake_kernel(path_px: float, steps: int = 256) -> np.ndarray:
    """A curved camera-shake path (random walk with momentum and the odd jerk), drawn into a blur kernel."""
    theta = np.random.uniform(0, 2 * np.pi) + np.cumsum(np.random.normal(0, 0.1, steps))
    jerks = (np.random.random(steps) < 0.02) * np.random.normal(0, 0.8, steps)
    theta = theta + np.cumsum(jerks)
    pts = np.cumsum(np.stack([np.cos(theta), np.sin(theta)], 1), 0) * (path_px / steps)   # path length = path_px
    pts -= pts.mean(0)
    r = int(np.ceil(np.abs(pts).max())) + 2
    k = np.zeros((2 * r + 1, 2 * r + 1), np.float32)
    for x, y in pts + r:                                          # each point spread over its 4 pixels
        x0, y0 = int(np.floor(x)), int(np.floor(y))
        fx, fy = x - x0, y - y0
        k[y0, x0] += (1 - fx) * (1 - fy)
        k[y0, x0 + 1] += fx * (1 - fy)
        k[y0 + 1, x0] += (1 - fx) * fy
        k[y0 + 1, x0 + 1] += fx * fy
    return k / k.sum()


def motion_blur_b(img: np.ndarray, path_px: float) -> np.ndarray:
    return _u8(cv2.filter2D(_f(img), -1, shake_kernel(path_px), borderType=cv2.BORDER_REFLECT))


def defocus_blur_b(img: np.ndarray, sigma_px: float) -> np.ndarray:
    x = cv2.GaussianBlur(_f(img), (0, 0), sigma_px, borderType=cv2.BORDER_REFLECT)
    h, w = x.shape[:2]
    shift = 0.2 * sigma_px                                        # colour fringes grow with the blur
    for c, dx in ((0, shift), (2, -shift)):                       # red one way, blue the other
        m = np.float32([[1, 0, dx], [0, 1, 0]])
        x[..., c] = cv2.warpAffine(x[..., c], m, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return _u8(x)


def low_light_b(img: np.ndarray, light: float, photons: int = 200) -> np.ndarray:
    x = _f(img)
    dark = np.random.poisson(x * light * photons) / photons       # few photons -> heavy grain
    out = (dark / light).astype(np.float32)                       # auto exposure: brighten all the way back
    out = cv2.GaussianBlur(out, (0, 0), 1.0)                      # the phone smooths the grain (and the detail)
    out *= np.float32([1.12, 1.0, 0.78])                          # warm street-light colour
    return _u8(out)


def compression_b(img: np.ndarray, badness: float) -> np.ndarray:
    scale = 1.0 / (1.0 + 0.5 * badness)                           # apps shrink photos more on worse settings ...
    quality = int(np.clip(round(90 * np.exp(-1.3 * badness)), 1, 100))   # ... and compress harder
    h, w = img.shape[:2]
    small = cv2.resize(img, (max(8, round(w * scale)), max(8, round(h * scale))), interpolation=cv2.INTER_AREA)
    buf = io.BytesIO()
    Image.fromarray(small).save(buf, "WEBP", quality=quality)
    buf.seek(0)
    back = np.array(Image.open(buf).convert("RGB"))
    return cv2.resize(back, (w, h), interpolation=cv2.INTER_CUBIC)


EFFECTS = {"gaussian_noise": sensor_noise_b, "motion_blur": motion_blur_b, "defocus_blur": defocus_blur_b,
           "low_light": low_light_b, "jpeg_compression": compression_b}
assert set(EFFECTS) == set(NOISE_TYPES) == set(KNOBS)


def apply_b(img: np.ndarray, noise: str, knob: float, seed: int) -> np.ndarray:
    """One recipe-B effect at an explicit knob value (used by the calibration)."""
    if img.dtype != np.uint8 or img.ndim != 3 or img.shape[2] != 3:
        raise ValueError("expected an RGB uint8 image (H x W x 3)")
    np.random.seed(seed)
    return EFFECTS[noise](img, float(knob))


def make_noisy_b(img: np.ndarray, noise: str, level: int, seed: int) -> np.ndarray:
    """One recipe-B effect at one of our levels (1, 2, 3), with the calibrated knob."""
    if PARAMS is None:
        raise RuntimeError("recipe B is not calibrated yet: run python scripts/make_recipe_b.py --calibrate")
    return apply_b(img, noise, PARAMS[noise][int(level)], seed)


# ----------------------------------------------------------------------------- SSIM (Wang et al. 2004)
def _grey(img: np.ndarray) -> np.ndarray:
    return img.astype(np.float64) @ np.array([0.299, 0.587, 0.114])


MS_WEIGHTS = np.array([0.0448, 0.2856, 0.3001, 0.2363, 0.1333])   # MS-SSIM scale weights (Wang et al. 2003)


def _ssim_terms(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """Mean luminance term and mean contrast-structure term of SSIM (11 x 11 Gaussian window, sigma 1.5)."""
    c1, c2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2

    def blur(z):
        return cv2.GaussianBlur(z, (11, 11), 1.5, borderType=cv2.BORDER_REFLECT)

    mx, my = blur(x), blur(y)
    vx, vy, cxy = blur(x * x) - mx * mx, blur(y * y) - my * my, blur(x * y) - mx * my
    lum = (2 * mx * my + c1) / (mx * mx + my * my + c1)
    cs = (2 * cxy + c2) / (vx + vy + c2)
    return float(lum.mean()), float(cs.mean())


def _ms_ssim(x: np.ndarray, y: np.ndarray) -> float:
    """Multi-scale SSIM: contrast-structure at 5 scales (each half the size of the last) + luminance at the coarsest."""
    css = []
    for i in range(len(MS_WEIGHTS)):
        lum, cs = _ssim_terms(x, y)
        css.append(max(cs, 1e-6))
        if i < len(MS_WEIGHTS) - 1:
            size = (x.shape[1] // 2, x.shape[0] // 2)
            x, y = cv2.resize(x, size, interpolation=cv2.INTER_AREA), cv2.resize(y, size, interpolation=cv2.INTER_AREA)
    return float(max(lum, 1e-6) ** MS_WEIGHTS[-1] * np.prod(np.array(css) ** MS_WEIGHTS))


def ssim(a: np.ndarray, b: np.ndarray, level: bool = True) -> float:
    """Levelled colour MS-SSIM: multi-scale structural similarity on each of the R, G and B channels, averaged.

    Multi-scale: the photos are also compared at 1/2, 1/4, 1/8 and 1/16 size, so blotchy noise (which
    hides the leaf) counts as much as fine grain (which the eye, and CLIP, mostly look through).
    level=True first stretches each channel of b to the overall brightness and contrast of the same channel
    of a, like a phone's auto exposure and white balance: a photo that is only darker or tinted does not
    count as damaged. Three simpler versions were dropped before anything was scored on recipe B (plain grey
    SSIM, levelled grey SSIM, levelled colour SSIM): each made recipe B's blotchy low light and sensor noise
    visibly harsher than the test images at the same score (docs/PROJECT_HISTORY.md).
    """
    out = []
    for c in range(3):
        x, y = a[..., c].astype(np.float64), b[..., c].astype(np.float64)
        if level:
            y = (y - y.mean()) * (x.std() / (y.std() + 1e-8)) + x.mean()
        out.append(_ms_ssim(x, y))
    return float(np.mean(out))
