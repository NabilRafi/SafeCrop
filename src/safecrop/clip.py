"""CLIP image encoder: loading, the exact Step 2 preprocessing, embeddings, partial unfreezing, checkpoints."""
from __future__ import annotations

import contextlib
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from tqdm.auto import tqdm

MEAN = (0.48145466, 0.4578275, 0.40821073)          # CLIP's normalisation (same numbers as the notebooks)
STD = (0.26862954, 0.26130258, 0.27577711)
TINY = "tiny-random"                                 # a small random CLIP for smoke tests (no download)


def pick_device(pref: str = "auto") -> torch.device:
    if pref and pref != "auto":
        return torch.device(pref)
    if torch.cuda.is_available():
        return torch.device("cuda")
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def load_clip(name: str):
    """A transformers CLIPModel (float32, eval mode). First use downloads the weights (~1.7 GB for ViT-L/14)."""
    from transformers import CLIPConfig, CLIPModel
    if name == TINY:
        torch.manual_seed(0)
        cfg = CLIPConfig(
            text_config=dict(vocab_size=1000, hidden_size=32, intermediate_size=64, num_hidden_layers=1,
                             num_attention_heads=2, max_position_embeddings=77,
                             bos_token_id=0, eos_token_id=1, pad_token_id=1),
            vision_config=dict(image_size=224, patch_size=32, hidden_size=48, intermediate_size=96,
                               num_hidden_layers=3, num_attention_heads=3),
            projection_dim=32)
        return CLIPModel(cfg).eval()
    return CLIPModel.from_pretrained(name).float().eval()


def load_tokenizer(name: str):
    if name == TINY:
        return None
    from transformers import AutoTokenizer
    return AutoTokenizer.from_pretrained(name)


class ImageEncoder(torch.nn.Module):
    """CLIP's image side: vision transformer -> projection -> unit-length vector (what the database compares)."""

    def __init__(self, clip):
        super().__init__()
        self.vision = clip.vision_model
        self.proj = clip.visual_projection
        self.size = int(clip.config.vision_config.image_size)
        self.dim = int(clip.config.projection_dim)
        self.register_buffer("mean", torch.tensor(MEAN).view(1, 3, 1, 1), persistent=False)
        self.register_buffer("std", torch.tensor(STD).view(1, 3, 1, 1), persistent=False)

    def pixels(self, x_uint8: torch.Tensor) -> torch.Tensor:
        """(B, H, W, 3) uint8 at the model's size -> normalised (B, 3, H, W) float."""
        x = x_uint8.permute(0, 3, 1, 2).float() / 255.0
        return (x - self.mean) / self.std

    def forward(self, x_uint8: torch.Tensor) -> torch.Tensor:
        v = self.proj(self.vision(pixel_values=self.pixels(x_uint8)).pooler_output)
        return F.normalize(v.float(), dim=-1)


def fit_size(img: np.ndarray, size: int) -> np.ndarray:
    """Step 2 preprocessing: shortest side -> size (bicubic), then the central size x size square.
    Test images are already 224 x 224, so for ViT-L/14 this changes nothing."""
    h, w = img.shape[:2]
    if (h, w) == (size, size):
        return img
    im = Image.fromarray(img)
    s = size / min(w, h)
    if s != 1:
        im = im.resize((max(size, round(w * s)), max(size, round(h * s))), Image.BICUBIC)
    w, h = im.size
    left, top = (w - size) // 2, (h - size) // 2
    return np.array(im.crop((left, top, left + size, top + size)))


def autocast(device: torch.device):
    """fp16 mixed precision on NVIDIA GPUs; plain float32 on Apple (mps) and CPU."""
    if device.type == "cuda":
        return torch.autocast("cuda", dtype=torch.float16)
    return contextlib.nullcontext()


@torch.no_grad()
def embed_arrays(encoder: ImageEncoder, arrays, device: torch.device, batch: int = 32,
                 desc: str | None = None) -> np.ndarray:
    """Unit-length embeddings (N, dim) float32 for a list of RGB uint8 arrays."""
    was_training = encoder.training
    encoder.eval()
    out = []
    it = range(0, len(arrays), batch)
    for i in (tqdm(it, desc=desc) if desc else it):
        x = np.stack([fit_size(a, encoder.size) for a in arrays[i:i + batch]])
        with autocast(device):
            out.append(encoder(torch.from_numpy(x).to(device)).float().cpu())
    encoder.train(was_training)
    return torch.cat(out).numpy() if out else np.zeros((0, encoder.dim), np.float32)


def embed_paths(encoder: ImageEncoder, paths, device: torch.device, batch: int = 32, desc: str | None = None):
    out = []
    for i in range(0, len(paths), 256):                # read in chunks to keep memory small
        arrays = [np.array(Image.open(p).convert("RGB")) for p in paths[i:i + 256]]
        out.append(embed_arrays(encoder, arrays, device, batch, desc=None))
        if desc:
            print(f"  {desc}: {min(i + 256, len(paths))}/{len(paths)}", flush=True)
    return np.concatenate(out) if out else np.zeros((0, encoder.dim), np.float32)


def sentences(row) -> list[str]:
    """The four CLIP sentences per option (Step 2): averaged into one text vector."""
    if row["key"].endswith("_healthy"):
        c = row["crop"]
        return [f"a photo of a healthy {c} plant.", f"a photo of healthy {c} leaves.",
                f"a close-up photo of a healthy {c} leaf.", f"a photo of a {c} plant with no disease."]
    n, c = row["clip_name"], row["crop"]
    return [f"a photo of {n}.", f"a photo of a plant with {n}.",
            f"a close-up photo of a leaf with {n}.", f"a photo of {c} plants affected by {n}."]


@torch.no_grad()
def text_vectors(clip, tokenizer, labels_df, device) -> np.ndarray:
    """One unit vector per option (33 x dim), in labels.csv order."""
    rows = []
    for _, r in labels_df.iterrows():
        t = tokenizer(sentences(r), padding=True, truncation=True, max_length=77, return_tensors="pt")
        v = clip.text_projection(clip.text_model(input_ids=t["input_ids"].to(device),
                                                 attention_mask=t["attention_mask"].to(device)).pooler_output)
        rows.append(F.normalize(v.float(), dim=-1).mean(0))
    T = torch.stack(rows)
    return F.normalize(T, dim=-1).cpu().numpy()


def set_trainable(encoder: ImageEncoder, unfreeze_last: int) -> int:
    """Freeze everything, then unfreeze the last N transformer blocks + final layer norm + projection.
    unfreeze_last = -1 trains the whole image encoder; 0 trains nothing. Returns the trainable count."""
    for p in encoder.parameters():
        p.requires_grad = False
    blocks = encoder.vision.encoder.layers
    if unfreeze_last < 0:
        for p in encoder.parameters():
            p.requires_grad = True
    elif unfreeze_last > 0:
        for blk in blocks[-unfreeze_last:]:
            for p in blk.parameters():
                p.requires_grad = True
        for p in list(encoder.vision.post_layernorm.parameters()) + list(encoder.proj.parameters()):
            p.requires_grad = True
    return sum(p.numel() for p in encoder.parameters() if p.requires_grad)


def save_checkpoint(encoder: ImageEncoder, file: Path, meta: dict) -> None:
    """Saves only the trained weights (small), plus the settings needed to rebuild the model."""
    state = {k: v.detach().cpu() for k, v in encoder.state_dict().items()
             if k in {n for n, p in encoder.named_parameters() if p.requires_grad}}
    torch.save({"meta": meta, "state": state}, file)


def load_checkpoint(file: Path, device: torch.device) -> tuple[ImageEncoder, dict]:
    ck = torch.load(file, map_location="cpu", weights_only=False)
    enc = ImageEncoder(load_clip(ck["meta"]["model"]))
    missing = set(ck["state"]) - set(enc.state_dict())
    assert not missing, f"checkpoint has unknown weights: {sorted(missing)[:3]}"
    enc.load_state_dict(ck["state"], strict=False)
    return enc.to(device).eval(), ck["meta"]
