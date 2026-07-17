#!/usr/bin/env python3
"""Minimal reproduction harness for timm Attention2d / MultiQueryAttention2d.

The reported failure is ROCm-specific. This script exercises the same forward
paths on the best available local device and records whether ROCm is present.
"""

from __future__ import annotations

import json
import os
import platform
import sys
import traceback
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
if str(CODEBASE) not in sys.path:
    sys.path.insert(0, str(CODEBASE))


def _torch_info(torch):
    return {
        "torch_version": torch.__version__,
        "torch_cuda": torch.version.cuda,
        "torch_hip": getattr(torch.version, "hip", None),
        "cuda_available": torch.cuda.is_available(),
        "cuda_device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
        "platform": platform.platform(),
        "python": sys.version,
    }


def _select_device(torch):
    if getattr(torch.version, "hip", None) and torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def _run_attention2d(torch, device):
    from timm.layers.attention2d import Attention2d, MultiQueryAttention2d

    x = torch.randn(1, 128, 32, 48, device=device)
    mask = torch.randint(0, 2, size=(32 * 48, 32 * 48), dtype=torch.float32, device=device)

    cases = [
        {"bias": True, "expand_first": True, "head_first": True, "attn_mask": True},
        {"bias": False, "expand_first": False, "head_first": False, "attn_mask": False},
    ]

    results = []
    for case in cases:
        attn = Attention2d(
            128,
            128,
            num_heads=4,
            bias=case["bias"],
            expand_first=case["expand_first"],
            head_first=case["head_first"],
        ).to(device)
        attn.eval()
        try:
            out = attn(x, mask if case["attn_mask"] else None)
            results.append(
                {
                    "module": "Attention2d",
                    "case": case,
                    "shape": list(out.shape),
                    "ok": True,
                }
            )
        except Exception as exc:  # pragma: no cover - evidence capture
            results.append(
                {
                    "module": "Attention2d",
                    "case": case,
                    "ok": False,
                    "error": f"{type(exc).__name__}: {exc}",
                    "traceback": traceback.format_exc(),
                }
            )

    mqa = MultiQueryAttention2d(128, 128, num_heads=4, key_dim=32, value_dim=32).to(device)
    mqa.eval()
    try:
        out = mqa(x)
        results.append(
            {
                "module": "MultiQueryAttention2d",
                "case": {"key_dim": 32, "value_dim": 32, "kv_stride": 1, "query_strides": 1},
                "shape": list(out.shape),
                "ok": True,
            }
        )
    except Exception as exc:  # pragma: no cover - evidence capture
        results.append(
            {
                "module": "MultiQueryAttention2d",
                "case": {"key_dim": 32, "value_dim": 32, "kv_stride": 1, "query_strides": 1},
                "ok": False,
                "error": f"{type(exc).__name__}: {exc}",
                "traceback": traceback.format_exc(),
            }
        )

    return results


def main() -> int:
    import torch

    info = _torch_info(torch)
    device = _select_device(torch)

    print(json.dumps({"event": "runtime_info", **info}, sort_keys=True))
    print(json.dumps({"event": "selected_device", "device": str(device)}, sort_keys=True))

    if device.type != "cuda":
        print(
            json.dumps(
                {
                    "event": "blocking_reason",
                    "reason": (
                        "ROCm is not available in this environment, so the reported "
                        "HIP error cannot be exercised locally."
                    ),
                },
                sort_keys=True,
            )
        )

    results = _run_attention2d(torch, device)
    print(json.dumps({"event": "results", "results": results}, sort_keys=True))

    has_failure = any(not item.get("ok", False) for item in results)
    if has_failure:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
