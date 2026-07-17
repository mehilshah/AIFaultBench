#!/usr/bin/env python3
"""Minimal repro for the PyG cuda:1 PNAConv failure reported in #9933.

The repro is intentionally tiny:
- it uses the local `codebase/` snapshot via `sys.path`
- it checks that a multi-GPU CUDA environment is present
- it runs a single `PNAConv` forward pass on `cuda:1`

In this standardized workspace the run is expected to be blocked because only
one GPU is visible. On a machine with at least two CUDA devices, this script
targets the reported failure mode directly.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
TARGET_DEVICE_INDEX = 1


def emit(payload: Dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def main() -> int:
    os.environ.setdefault("CUDA_LAUNCH_BLOCKING", "1")

    try:
        import torch
    except Exception as exc:  # pragma: no cover - environment dependent
        payload = {
            "status": "blocked",
            "reason": f"torch import failed: {exc}",
            "reproducible": False,
        }
        emit(payload)
        return 2

    payload = {
        "python": sys.version.split()[0],
        "torch": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "cuda_device_count": torch.cuda.device_count(),
        "target_device": f"cuda:{TARGET_DEVICE_INDEX}",
        "codebase": str(CODEBASE),
    }

    if not torch.cuda.is_available():
        payload.update(
            status="blocked",
            reason="CUDA is not available in this environment.",
            reproducible=False,
        )
        emit(payload)
        return 2

    if torch.cuda.device_count() <= TARGET_DEVICE_INDEX:
        payload.update(
            status="blocked",
            reason=(
                "Need at least two visible CUDA devices to probe cuda:1, "
                f"but only {torch.cuda.device_count()} device(s) are visible."
            ),
            reproducible=False,
        )
        emit(payload)
        return 2

    sys.path.insert(0, str(CODEBASE))

    from torch_geometric.data import Data
    from torch_geometric.nn import PNAConv

    device = torch.device(f"cuda:{TARGET_DEVICE_INDEX}")
    torch.cuda.set_device(device)

    # Small synthetic graph that still exercises the same PNAConv path as the
    # original report.
    x = torch.tensor(
        [
            [1.0, 0.0],
            [0.0, 1.0],
            [1.0, 1.0],
            [0.5, 0.5],
        ]
    )
    edge_index = torch.tensor(
        [
            [0, 1, 2, 3, 0, 2, 1, 3],
            [1, 0, 3, 2, 2, 0, 3, 1],
        ],
        dtype=torch.long,
    )
    edge_attr = torch.tensor([[0.1], [0.2], [0.3], [0.4], [0.5], [0.6], [0.7],
                              [0.8]])
    data = Data(x=x, edge_index=edge_index, edge_attr=edge_attr).to(device)

    # Degree histogram stays on CPU in the report; that is the configuration we
    # want to preserve here.
    deg = torch.bincount(data.edge_index[1].cpu(), minlength=data.num_nodes)
    deg_hist = torch.bincount(deg, minlength=int(deg.max()) + 1)

    conv = PNAConv(
        in_channels=2,
        out_channels=2,
        aggregators=["mean", "min", "max", "std"],
        scalers=["identity", "amplification", "attenuation"],
        deg=deg_hist,
        edge_dim=1,
        towers=2,
        pre_layers=1,
        post_layers=1,
        divide_input=False,
    ).to(device)

    try:
        out = conv(data.x, data.edge_index, data.edge_attr)
        torch.cuda.synchronize(device)
        emit(
            {
                **payload,
                "status": "completed",
                "reproducible": False,
                "output_shape": list(out.shape),
                "note": (
                    "Forward pass completed without an illegal memory access "
                    "on the current hardware."
                ),
            }
        )
        return 0
    except RuntimeError as exc:
        message = str(exc)
        reproduced = "illegal memory access" in message.lower()
        emit(
            {
                **payload,
                "status": "failed",
                "reproducible": reproduced,
                "error": message,
            }
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
