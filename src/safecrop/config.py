"""Settings: configs/default.yaml, then an optional --config file, then --set key=value overrides."""
from __future__ import annotations

import argparse
import copy
import datetime as _dt
import json
import os
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]          # the repo folder (…/safecrop-clip-finetune)


def _merge(base: dict, extra: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in (extra or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


def _set(cfg: dict, dotted: str, value: str) -> None:
    keys = dotted.split(".")
    d = cfg
    for k in keys[:-1]:
        if k not in d or not isinstance(d[k], dict):
            raise KeyError(f"unknown setting '{dotted}'")
        d = d[k]
    if keys[-1] not in d:
        raise KeyError(f"unknown setting '{dotted}' (see configs/default.yaml for the names)")
    d[keys[-1]] = yaml.safe_load(value)               # "5" -> 5, "[0,1]" -> [0, 1], "true" -> True


def load_config(config_file: str | None = None, overrides: list[str] | None = None) -> dict:
    cfg = yaml.safe_load(open(ROOT / "configs" / "default.yaml"))
    if config_file:
        p = Path(config_file)
        cfg = _merge(cfg, yaml.safe_load(open(p if p.is_absolute() else ROOT / p)) or {})
    for item in overrides or []:
        if "=" not in item:
            raise ValueError(f"--set expects key=value, got '{item}'")
        k, v = item.split("=", 1)
        _set(cfg, k.strip(), v.strip())
    return cfg


def cli(description: str, extra=None) -> tuple[argparse.Namespace, dict]:
    """Common command line: --config FILE, --set key=value (repeatable), --tag NAME."""
    ap = argparse.ArgumentParser(description=description)
    ap.add_argument("--config", default=None, help="extra YAML on top of configs/default.yaml, e.g. configs/smoke.yaml")
    ap.add_argument("--set", action="append", default=[], metavar="KEY=VALUE",
                    help="override one setting, e.g. --set finetune.epochs=5 (repeatable)")
    ap.add_argument("--tag", default="", help="short name added to the results folder")
    if extra:
        extra(ap)
    args = ap.parse_args()
    return args, load_config(args.config, args.set)


def path(cfg_value: str) -> Path:
    p = Path(cfg_value)
    return p if p.is_absolute() else ROOT / p


def model_slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower().split("/")[-1]).strip("-")


def new_run_dir(cfg: dict, experiment: str, tag: str = "") -> Path:
    stamp = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    name = "_".join(x for x in [stamp, model_slug(cfg["model"]), re.sub(r"[^A-Za-z0-9_-]+", "-", tag)] if x)
    d = path(cfg["results_dir"]) / experiment / name
    i = 2
    while d.exists():                                   # two runs in the same second: add -2, -3, ...
        d = d.with_name(f"{name}-{i}")
        i += 1
    d.mkdir(parents=True)
    with open(d / "config.yaml", "w") as f:
        yaml.safe_dump(cfg, f, sort_keys=False)
    return d


def cache_dir(cfg: dict) -> Path:
    d = path(cfg["results_dir"]) / "cache" / model_slug(cfg["model"])
    d.mkdir(parents=True, exist_ok=True)
    return d


def dump_json(obj, p: Path) -> None:
    with open(p, "w") as f:
        json.dump(obj, f, indent=1, default=float)


def env_report() -> str:
    import platform
    import numpy
    import torch
    try:
        import transformers
        tv = transformers.__version__
    except Exception:                                  # pragma: no cover
        tv = "not installed"
    return (f"python {platform.python_version()} | torch {torch.__version__} | transformers {tv} | "
            f"numpy {numpy.__version__} | {platform.system()} {platform.machine()}")


os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
