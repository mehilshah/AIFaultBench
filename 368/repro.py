#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
import traceback
from pathlib import Path
from typing import Any, Dict

import torch

ROOT_DIR = Path(__file__).resolve().parent
import sys

sys.path.insert(0, str(ROOT_DIR / "codebase"))

import timm  # noqa: E402
from timm.models.convnext import ConvNeXtBlock  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark ConvNeXt forward timing.")
    parser.add_argument("--mode", choices=("auto", "full", "block"), default="auto")
    parser.add_argument("--iters", type=int, default=3)
    parser.add_argument("--warmup", type=int, default=1)
    parser.add_argument("--image-size", type=int, default=320)
    return parser.parse_args()


def benchmark(module: torch.nn.Module, sample: torch.Tensor, *, iters: int, warmup: int) -> float:
    module.eval()
    with torch.no_grad():
        for _ in range(warmup):
            module(sample)
        torch.cuda.synchronize()
        start = time.perf_counter()
        for _ in range(iters):
            module(sample)
        torch.cuda.synchronize()
        end = time.perf_counter()
    return (end - start) / iters


def patched_forward(self: ConvNeXtBlock, x: torch.Tensor) -> torch.Tensor:
    shortcut = x
    x = self.conv_dw(x.contiguous())
    if self.use_conv_mlp:
        x = self.norm(x)
        x = self.mlp(x)
    else:
        x = x.permute(0, 2, 3, 1).contiguous()
        x = self.norm(x)
        x = self.mlp(x)
        x = x.permute(0, 3, 1, 2).contiguous()
    if self.gamma is not None:
        x = x.mul(self.gamma.reshape(1, -1, 1, 1))
    x = self.drop_path(x) + self.shortcut(shortcut)
    return x


def run_full_benchmark(*, image_size: int, iters: int, warmup: int) -> Dict[str, Any]:
    sample = torch.randn(1, 3, image_size, image_size, device="cuda")
    model = timm.create_model(
        "convnext_large_in22ft1k",
        pretrained=False,
        features_only=True,
        out_indices=(1, 2, 3),
    ).cuda()
    baseline = benchmark(model, sample, iters=iters, warmup=warmup)

    original_forward = ConvNeXtBlock.forward
    ConvNeXtBlock.forward = patched_forward
    try:
        patched_model = timm.create_model(
            "convnext_large_in22ft1k",
            pretrained=False,
            features_only=True,
            out_indices=(1, 2, 3),
        ).cuda()
        patched = benchmark(patched_model, sample, iters=iters, warmup=warmup)
    finally:
        ConvNeXtBlock.forward = original_forward

    return {
        "mode": "full",
        "model_name": "convnext_large_in22ft1k",
        "input_shape": [1, 3, image_size, image_size],
        "baseline_seconds": baseline,
        "patched_seconds": patched,
        "ratio": baseline / patched if patched else None,
    }


def run_block_benchmark(*, iters: int, warmup: int) -> Dict[str, Any]:
    sample = torch.randn(1, 384, 20, 20, device="cuda")
    block = ConvNeXtBlock(384, 384, conv_mlp=False).cuda()
    baseline = benchmark(block, sample, iters=iters, warmup=warmup)

    original_forward = ConvNeXtBlock.forward
    ConvNeXtBlock.forward = patched_forward
    try:
        patched_block = ConvNeXtBlock(384, 384, conv_mlp=False).cuda()
        patched = benchmark(patched_block, sample, iters=iters, warmup=warmup)
    finally:
        ConvNeXtBlock.forward = original_forward

    return {
        "mode": "block",
        "block_shape": [1, 384, 20, 20],
        "baseline_seconds": baseline,
        "patched_seconds": patched,
        "ratio": baseline / patched if patched else None,
    }


def main() -> int:
    args = parse_args()

    device_name = torch.cuda.get_device_name(0)
    torch_version = torch.__version__
    print(f"torch={torch_version}")
    print(f"cuda_device={device_name}")

    result: Dict[str, Any] = {
        "torch_version": torch_version,
        "cuda_device": device_name,
    }

    try:
        if args.mode == "full":
            result.update(run_full_benchmark(image_size=args.image_size, iters=args.iters, warmup=args.warmup))
        elif args.mode == "block":
            result.update(run_block_benchmark(iters=args.iters, warmup=args.warmup))
        else:
            try:
                result.update(run_full_benchmark(image_size=args.image_size, iters=args.iters, warmup=args.warmup))
            except Exception as full_exc:  # pragma: no cover - fallback path for other hosts
                result["full_error"] = "".join(traceback.format_exception(type(full_exc), full_exc, full_exc.__traceback__))
                result.update(run_block_benchmark(iters=args.iters, warmup=args.warmup))
    except Exception as exc:
        print("benchmark_failed")
        print("".join(traceback.format_exception(type(exc), exc, exc.__traceback__)))
        return 1

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
