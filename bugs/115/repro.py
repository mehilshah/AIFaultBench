#!/usr/bin/env python3
"""Minimal reproduction for axolotl sweep output_dir reuse."""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent
CODEBASE_SRC = ROOT / "codebase" / "src"
BASE_CONFIG = ROOT / "base_config.yml"
SWEEP_CONFIG = ROOT / "sweep.yml"


def main() -> int:
    sweeps_path = CODEBASE_SRC / "axolotl" / "cli" / "utils" / "sweeps.py"
    spec = importlib.util.spec_from_file_location("axolotl_sweeps", sweeps_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load sweep generator from {sweeps_path}")
    sweeps_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sweeps_module)
    generate_sweep_configs = sweeps_module.generate_sweep_configs

    output_dirs: list[str | None] = []
    sweep_summaries: list[dict[str, object]] = []

    with open(BASE_CONFIG, "r", encoding="utf-8") as fin:
        base_config = yaml.safe_load(fin)
    with open(SWEEP_CONFIG, "r", encoding="utf-8") as fin:
        sweep_config = yaml.safe_load(fin)

    for cfg in generate_sweep_configs(base_config, sweep_config):
        output_dirs.append(cfg.get("output_dir"))
        sweep_summaries.append(
            {
                "learning_rate": cfg.get("learning_rate"),
                "lora_r": cfg.get("lora_r"),
                "lora_alpha": cfg.get("lora_alpha"),
                "load_in_8bit": cfg.get("load_in_8bit"),
                "output_dir": cfg.get("output_dir"),
            }
        )

    unique_output_dirs = sorted({value for value in output_dirs if value is not None})
    print(f"base_config: {BASE_CONFIG.name}")
    print(f"sweep_config: {SWEEP_CONFIG.name}")
    print(f"permutations_generated: {len(output_dirs)}")
    print(f"unique_output_dirs: {len(unique_output_dirs)}")
    print(f"output_dirs: {unique_output_dirs if unique_output_dirs else output_dirs}")
    print("sample_permutations:")
    for summary in sweep_summaries[:5]:
        print(summary)

    if len(output_dirs) > 1 and len(unique_output_dirs) == 1:
        print(
            "BUG_REPRODUCED: all sweep permutations reuse the same output_dir "
            f"({unique_output_dirs[0]})."
        )
        return 0

    print("BUG_NOT_REPRODUCED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
