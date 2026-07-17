#!/usr/bin/env python3
"""Reproduce diffusers issue 14146 for Krea2Pipeline on ROCm/gfx1201.

This script intentionally runs the report's exact code path when a GPU backend is
available. In CPU-only environments it exits early with a blocking reason so the
bundle remains honest about reproducibility.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def main() -> int:
    try:
        import torch
    except Exception as exc:  # pragma: no cover - environment specific
        print(f"torch_import_failed: {exc}", file=sys.stderr)
        return 2

    torch_info = {
        "torch_version": torch.__version__,
        "cuda_available": bool(torch.cuda.is_available()),
        "hip_version": getattr(torch.version, "hip", None),
        "cuda_version": getattr(torch.version, "cuda", None),
    }
    print(json.dumps(torch_info, sort_keys=True))

    if getattr(torch.version, "hip", None) is None:
        print(
            "blocking_reason: this repro requires a ROCm build of PyTorch on gfx1201; "
            "the local environment is not ROCm.",
            file=sys.stderr,
        )
        return 2

    # Import diffusers only after the GPU gate so the script can still be used as
    # a clean blocker on CPU-only hosts.
    from diffusers import Krea2Pipeline

    torch._dynamo.config.recompile_limit = 8192
    torch.set_float32_matmul_precision("high")

    max_memory = {0: "13GB"}
    model_id = os.environ.get("KREA2_MODEL_ID", "krea/Krea-2-Turbo")
    out_path = Path(os.environ.get("KREA2_OUTPUT", "krea2.png"))

    pipe = Krea2Pipeline.from_pretrained(
        model_id,
        torch_dtype=torch.bfloat16,
        max_memory=max_memory,
    )
    pipe.enable_sequential_cpu_offload()
    pipe.transformer.compile()

    prompt = "a photograph of a potato"
    image = pipe(
        prompt,
        height=1024,
        width=1024,
        num_inference_steps=8,
        guidance_scale=0,
        generator=torch.Generator("cuda").manual_seed(0),
    ).images[0]
    image.save(out_path)

    print(
        json.dumps(
            {
                "saved_image": str(out_path),
                "image_size": getattr(image, "size", None),
                "backend": "cuda" if torch.cuda.is_available() else "cpu",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
