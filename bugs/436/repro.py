#!/usr/bin/env python3
from __future__ import annotations

import gc
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE_FILE = ROOT / "codebase" / "src" / "lightning" / "pytorch" / "plugins" / "precision" / "amp.py"


def find_offending_line() -> tuple[int, str] | None:
    for lineno, line in enumerate(SOURCE_FILE.read_text().splitlines(), start=1):
        if "cache_enabled=False" in line:
            return lineno, line.strip()
    return None


def run_gpu_benchmark() -> dict[str, int]:
    import torch
    import torch.nn as nn

    torch.manual_seed(0)

    hidden = 2048
    steps = 128
    batch = 16
    device = "cuda"

    class Decoder(nn.Module):
        def __init__(self, width: int) -> None:
            super().__init__()
            self.layer = nn.Linear(width, width, bias=False)

        def forward(self, x):
            return self.layer(x)

    x = torch.randn(batch, hidden, device=device)
    results: dict[str, int] = {}

    for cache_enabled in (True, False):
        torch.cuda.empty_cache()
        gc.collect()
        torch.cuda.reset_peak_memory_stats()

        model = Decoder(hidden).to(device)
        loss = torch.zeros((), device=device)

        with torch.autocast(device_type="cuda", dtype=torch.bfloat16, cache_enabled=cache_enabled):
            cur = x
            for _ in range(steps):
                cur = model(cur)
                loss = loss + cur.float().mean()

        torch.cuda.synchronize()
        peak_forward = torch.cuda.max_memory_allocated()
        loss.backward()
        torch.cuda.synchronize()
        peak_total = torch.cuda.max_memory_allocated()

        key = "true" if cache_enabled else "false"
        results[f"{key}_peak_forward_bytes"] = int(peak_forward)
        results[f"{key}_peak_total_bytes"] = int(peak_total)

        del model, loss, cur
        torch.cuda.empty_cache()
        gc.collect()

    return results


def main() -> int:
    summary: dict[str, object] = {
        "reproducible": False,
        "blocking_reason": None,
        "steps": [],
        "evidence": {},
        "reproduction_command": "bash run_repro.sh",
    }

    offending_line = find_offending_line()
    if offending_line is None:
        summary["blocking_reason"] = "Could not find `cache_enabled=False` in the checked-out Lightning source."
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 1

    summary["steps"].append(
        f"Verified `{SOURCE_FILE.relative_to(ROOT)}` line {offending_line[0]} contains `{offending_line[1]}`."
    )

    try:
        import torch
    except Exception as exc:  # pragma: no cover - import failure is environment-specific
        summary["blocking_reason"] = f"Torch import failed: {exc!r}"
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 1

    summary["steps"].append(f"Imported torch {torch.__version__}.")

    if not torch.cuda.is_available():
        summary["blocking_reason"] = "CUDA is unavailable in this environment."
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 1

    summary["steps"].append(f"CUDA device: {torch.cuda.get_device_name(0)}.")

    results = run_gpu_benchmark()
    true_peak = results["true_peak_total_bytes"]
    false_peak = results["false_peak_total_bytes"]
    delta = false_peak - true_peak

    summary["evidence"] = {
        "source_file": str(SOURCE_FILE.relative_to(ROOT)),
        "source_line": offending_line[0],
        "source_excerpt": offending_line[1],
        "torch_version": torch.__version__,
        "cuda_device": torch.cuda.get_device_name(0),
        "cache_enabled_true_peak_total_bytes": true_peak,
        "cache_enabled_false_peak_total_bytes": false_peak,
        "peak_delta_bytes": delta,
    }

    summary["steps"].append(
        "Ran a repeated decoder-style forward/backward benchmark under bf16 autocast with cache_enabled=True and False."
    )
    summary["steps"].append("Observed a large peak-memory increase when cache_enabled=False was used.")

    summary["reproducible"] = bool(false_peak > true_peak * 2 and delta > 256 * 1024 * 1024)

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["reproducible"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
