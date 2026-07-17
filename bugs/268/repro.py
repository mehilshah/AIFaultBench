#!/usr/bin/env python3
"""Reproduce the diffusers LoRA offline/local-files-only regression.

Each invocation runs exactly one case so that `HF_HUB_OFFLINE` is read before
diffusers and huggingface_hub are imported.
"""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path


def run_case(case: str) -> None:
    if case == "offline":
        os.environ["HF_HUB_OFFLINE"] = "1"
    else:
        os.environ.pop("HF_HUB_OFFLINE", None)

    import torch
    from safetensors.torch import save_file
    from diffusers.loaders import StableDiffusionLoraLoaderMixin

    print(f"case={case}")
    print(f"HF_HUB_OFFLINE={os.environ.get('HF_HUB_OFFLINE', '<unset>')}")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        weight_path = tmp_path / "adapter.safetensors"
        save_file({"unet.test.lora_A.weight": torch.ones(1)}, str(weight_path))
        print(f"created_weight={weight_path}")

        kwargs = {}
        if case == "local_files_only":
            kwargs["local_files_only"] = True

        try:
            StableDiffusionLoraLoaderMixin.lora_state_dict(tmpdir, **kwargs)
        except Exception as exc:  # noqa: BLE001
            print(f"{type(exc).__name__}: {exc}")
            raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--case",
        choices=("offline", "local_files_only"),
        required=True,
        help="Which reproduction path to execute.",
    )
    args = parser.parse_args()

    run_case(args.case)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
