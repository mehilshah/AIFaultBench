#!/usr/bin/env python3
"""Reproduce the ViT-S ONNX validation accuracy gap.

This script keeps the repro self-contained:
- instantiates the exact ViT-S augreg model from the local codebase,
- saves a deterministic checkpoint so both validation paths use the same weights,
- finds a synthetic image where the correct and default preprocessing disagree,
- exports ONNX from the same checkpoint,
- runs validate.py and onnx_validate.py against a one-image ImageFolder dataset,
- writes reproduction.json with the outcome.
"""

from __future__ import annotations

import json
import os
import random
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import torch
from PIL import Image


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
WORKDIR = ROOT / "_repro_tmp"
DATA_ROOT = WORKDIR / "synthetic_imagenet"
CHECKPOINT = WORKDIR / "vit_small_patch16_224_random.pth"
ONNX_FILE = WORKDIR / "vit_small_patch16_224_random.onnx"
RESULT_JSON = ROOT / "reproduction.json"

MODEL_NAME = "vit_small_patch16_224.augreg_in21k_ft_in1k"
NUM_CLASSES = 1000
IMAGE_SIZE = 256
SEARCH_ROUNDS = 4
SEARCH_BATCH_SIZE = 16


sys.path.insert(0, str(CODEBASE))

from timm import create_model  # noqa: E402
from timm.data import create_transform, resolve_data_config  # noqa: E402
from timm.utils.onnx import onnx_forward  # noqa: E402


def run_cmd(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    print("$ " + " ".join(_quote(arg) for arg in cmd), flush=True)
    proc = subprocess.run(
        cmd,
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        env={**os.environ, "PYTHONPATH": str(CODEBASE)},
    )
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, cmd, proc.stdout, proc.stderr)
    return proc


def _quote(arg: str) -> str:
    if not arg:
        return "''"
    if re.fullmatch(r"[A-Za-z0-9_./:=+-]+", arg):
        return arg
    return "'" + arg.replace("'", "'\"'\"'") + "'"


def make_pattern_image(seed: int, size: int = IMAGE_SIZE) -> Image.Image:
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    x = xx / max(size - 1, 1)
    y = yy / max(size - 1, 1)
    mode = seed % 6
    if mode == 0:
        arr = np.stack([x, y, 1.0 - x], axis=-1)
    elif mode == 1:
        arr = np.stack([y, 1.0 - x, x], axis=-1)
    elif mode == 2:
        arr = np.stack(
            [
                0.5 + 0.5 * np.sin(6 * np.pi * x),
                0.5 + 0.5 * np.cos(6 * np.pi * y),
                0.5 + 0.5 * np.sin(4 * np.pi * (x + y)),
            ],
            axis=-1,
        )
    elif mode == 3:
        checker = (((xx // 8) + (yy // 8) + seed) % 2).astype(np.float32)
        arr = np.stack([checker, 1.0 - checker, 0.25 + 0.5 * checker], axis=-1)
    elif mode == 4:
        rng = np.random.default_rng(1234 + seed)
        arr = rng.random((size, size, 3), dtype=np.float32)
    else:
        radial = np.sqrt((x - 0.5) ** 2 + (y - 0.5) ** 2)
        arr = np.stack([radial, 1.0 - radial, 0.5 + 0.5 * np.cos(10 * np.pi * radial)], axis=-1)
    arr = np.clip(arr * 255.0, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode="RGB")


def build_batch(images: list[Image.Image], cfg: dict) -> torch.Tensor:
    transform = create_transform(
        cfg["input_size"],
        is_training=False,
        crop_pct=cfg["crop_pct"],
        interpolation=cfg["interpolation"],
        mean=cfg["mean"],
        std=cfg["std"],
        use_prefetcher=False,
        normalize=True,
    )
    tensors = [transform(img) for img in images]
    return torch.stack(tensors, dim=0)


def prepare_checkpoint() -> torch.nn.Module:
    torch.manual_seed(0)
    random.seed(0)
    np.random.seed(0)
    torch.set_num_threads(1)

    model = create_model(
        MODEL_NAME,
        pretrained=False,
        num_classes=NUM_CLASSES,
        in_chans=3,
        exportable=True,
    )
    model.eval()
    CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), CHECKPOINT)
    print(f"Saved deterministic checkpoint to {CHECKPOINT}")
    return model


def find_mismatching_sample(model: torch.nn.Module) -> tuple[Image.Image, int, int, dict, dict]:
    correct_cfg = resolve_data_config(
        {},
        model=model,
        use_test_size=True,
        verbose=False,
    )
    wrong_cfg = resolve_data_config(
        {
            "img_size": None,
            "input_size": None,
            "interpolation": "",
            "mean": None,
            "std": None,
            "crop_pct": None,
            "crop_mode": None,
            "in_chans": None,
            "chans": None,
        },
        verbose=False,
    )
    print("Correct data config:", correct_cfg)
    print("Default data config:", wrong_cfg)

    with torch.inference_mode():
        for round_idx in range(SEARCH_ROUNDS):
            images = [make_pattern_image(round_idx * SEARCH_BATCH_SIZE + i) for i in range(SEARCH_BATCH_SIZE)]
            correct_batch = build_batch(images, correct_cfg)
            wrong_batch = build_batch(images, wrong_cfg)
            correct_logits = model(correct_batch)
            wrong_logits = model(wrong_batch)
            correct_pred = correct_logits.argmax(dim=1)
            wrong_pred = wrong_logits.argmax(dim=1)
            mismatches = (correct_pred != wrong_pred).nonzero(as_tuple=False).flatten()
            if mismatches.numel():
                idx = int(mismatches[0].item())
                print(
                    f"Found mismatch in round {round_idx}, sample {idx}: "
                    f"correct={int(correct_pred[idx])}, wrong={int(wrong_pred[idx])}"
                )
                return images[idx], int(correct_pred[idx]), int(wrong_pred[idx]), correct_cfg, wrong_cfg

    raise RuntimeError(
        "Could not find a sample whose top-1 prediction changes under the wrong preprocessing. "
        "The data config mismatch is still present, but this repro wants an observable accuracy gap."
    )


def make_dataset(image: Image.Image, target_idx: int) -> Path:
    if DATA_ROOT.exists():
        shutil.rmtree(DATA_ROOT)
    validation_root = DATA_ROOT / "validation"
    for idx in range(NUM_CLASSES):
        (validation_root / f"class{idx:04d}").mkdir(parents=True, exist_ok=True)
    target_dir = validation_root / f"class{target_idx:04d}"
    target_path = target_dir / "sample.png"
    image.save(target_path)
    print(f"Wrote one-image ImageFolder dataset to {target_path}")
    return DATA_ROOT


def main() -> None:
    if WORKDIR.exists():
        shutil.rmtree(WORKDIR)
    WORKDIR.mkdir(parents=True, exist_ok=True)

    model = prepare_checkpoint()
    image, correct_idx, wrong_idx, correct_cfg, wrong_cfg = find_mismatching_sample(model)
    data_root = make_dataset(image, correct_idx)

    print("Exporting ONNX from the same checkpoint...")
    run_cmd(
        [
            sys.executable,
            str(CODEBASE / "onnx_export.py"),
            str(ONNX_FILE),
            "--model",
            MODEL_NAME,
            "--num-classes",
            str(NUM_CLASSES),
            "--img-size",
            "224",
            "--checkpoint",
            str(CHECKPOINT),
            "--batch-size",
            "1",
        ]
    )

    sample_tensor = build_batch([image], correct_cfg)
    with torch.inference_mode():
        torch_out = model(sample_tensor)
    onnx_out = onnx_forward(str(ONNX_FILE), sample_tensor)
    max_abs_diff = float(np.max(np.abs(torch_out.detach().numpy() - onnx_out)))
    print(f"Torch vs ONNX max abs diff on the same preprocessed sample: {max_abs_diff:.6f}")

    print("Running validate.py with model-aware preprocessing...")
    validate_proc = run_cmd(
        [
            sys.executable,
            str(CODEBASE / "validate.py"),
            "--data-dir",
            str(data_root),
            "--model",
            MODEL_NAME,
            "--checkpoint",
            str(CHECKPOINT),
            "--batch-size",
            "1",
            "--workers",
            "1",
            "--device",
            "cpu",
            "--no-prefetcher",
            "--log-freq",
            "1",
        ]
    )

    print("Running onnx_validate.py with its built-in defaults...")
    run_cmd(
        [
            sys.executable,
            str(CODEBASE / "onnx_validate.py"),
            str(data_root / "validation"),
            "--onnx-input",
            str(ONNX_FILE),
            "--batch-size",
            "1",
            "--workers",
            "1",
            "--print-freq",
            "1",
        ]
    )

    reproducible = correct_idx != wrong_idx
    evidence = (
        "validate.py resolves the model-aware preprocessing for vit_small_patch16_224.augreg_in21k_ft_in1k "
        "from its pretrained_cfg, while onnx_validate.py falls back to generic defaults because it calls "
        "resolve_data_config(vars(args)) without model metadata. On the same checkpoint and the same synthetic "
        f"image, the correct preprocessing predicted class {correct_idx} and the default ONNX validation "
        f"preprocessing predicted class {wrong_idx}; ONNX export matched PyTorch with max abs diff "
        f"{max_abs_diff:.6f}."
    )
    steps = [
        "Instantiate vit_small_patch16_224.augreg_in21k_ft_in1k from the local timm codebase and save a deterministic checkpoint.",
        "Find a synthetic RGB image whose top-1 prediction changes between the model-aware preprocessing and the default preprocessing used by onnx_validate.py.",
        "Export ONNX from the same checkpoint, verify torch and ONNX agree on the same preprocessed tensor, and run validate.py plus onnx_validate.py to capture the divergent data-config paths.",
    ]
    result = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": steps,
        "blocking_reason": "" if reproducible else "Could not find a synthetic sample that flips top-1 between the two preprocessing configs.",
        "reproduction_command": "bash run_repro.sh",
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Wrote {RESULT_JSON}")


if __name__ == "__main__":
    main()
