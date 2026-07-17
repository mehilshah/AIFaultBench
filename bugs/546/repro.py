#!/usr/bin/env python3
"""Minimal reproducer for accelerate issue 1116.

The bug is in `accelerate.commands.launch.launch_command`: when a multi-node
config uses a single GPU id per node (for example `gpu_ids: "0"`), the launcher
turns `args.multi_gpu` off and falls back to `simple_launcher`, ignoring the
multi-node setup.
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent
CODEBASE_SRC = ROOT / "codebase" / "src"
sys.path.insert(0, str(CODEBASE_SRC))

from accelerate.commands.launch import launch_command, launch_command_parser  # noqa: E402
import accelerate.commands.launch as launch_mod  # noqa: E402


BASE_CONFIG = {
    "compute_environment": "LOCAL_MACHINE",
    "distributed_type": "MULTI_GPU",
    "mixed_precision": "no",
    "use_cpu": False,
    "dynamo_backend": "NO",
    "num_processes": 2,
    "num_machines": 2,
    "machine_rank": 0,
    "main_process_ip": "example",
    "main_process_port": 8888,
    "same_network": True,
}


def run_case(gpu_ids: str) -> dict:
    with tempfile.TemporaryDirectory(prefix=f"accelerate-bug-1116-{gpu_ids}-") as tmpdir:
        tmpdir = Path(tmpdir)
        config_path = tmpdir / "default_config.yaml"
        dummy_training = tmpdir / "dummy_training.py"
        dummy_training.write_text("print('dummy training script')\n", encoding="utf-8")

        config = dict(BASE_CONFIG)
        config["gpu_ids"] = gpu_ids
        config_path.write_text(yaml.safe_dump(config, sort_keys=True), encoding="utf-8")

        selected = {}
        original_simple = launch_mod.simple_launcher
        original_multi = launch_mod.multi_gpu_launcher

        def record_simple(args):
            selected["launcher"] = "simple_launcher"
            selected["multi_gpu"] = args.multi_gpu
            selected["num_machines"] = args.num_machines
            selected["gpu_ids"] = args.gpu_ids
            selected["nproc_per_node"] = getattr(args, "nproc_per_node", None)
            selected["nnodes"] = getattr(args, "nnodes", None)
            print(
                f"selected=simple_launcher multi_gpu={args.multi_gpu} num_machines={args.num_machines} "
                f"gpu_ids={args.gpu_ids} nproc_per_node={getattr(args, 'nproc_per_node', None)} "
                f"nnodes={getattr(args, 'nnodes', None)}"
            )

        def record_multi(args):
            selected["launcher"] = "multi_gpu_launcher"
            selected["multi_gpu"] = args.multi_gpu
            selected["num_machines"] = args.num_machines
            selected["gpu_ids"] = args.gpu_ids
            selected["nproc_per_node"] = getattr(args, "nproc_per_node", None)
            selected["nnodes"] = getattr(args, "nnodes", None)
            print(
                f"selected=multi_gpu_launcher multi_gpu={args.multi_gpu} num_machines={args.num_machines} "
                f"gpu_ids={args.gpu_ids} nproc_per_node={getattr(args, 'nproc_per_node', None)} "
                f"nnodes={getattr(args, 'nnodes', None)}"
            )

        launch_mod.simple_launcher = record_simple
        launch_mod.multi_gpu_launcher = record_multi
        try:
            parser = launch_command_parser()
            args = parser.parse_args(["--config_file", str(config_path), str(dummy_training)])
            launch_command(args)
        finally:
            launch_mod.simple_launcher = original_simple
            launch_mod.multi_gpu_launcher = original_multi

        if not selected:
            raise RuntimeError(f"launcher selection was not recorded for gpu_ids={gpu_ids!r}")
        return selected


def main() -> int:
    single = run_case("0")
    all_gpus = run_case("all")

    print("\nsummary")
    print(f"gpu_ids=0   -> {single['launcher']}")
    print(f"gpu_ids=all -> {all_gpus['launcher']}")

    if single["launcher"] != "simple_launcher":
        raise AssertionError("Expected gpu_ids='0' to take the simple_launcher path in the buggy version.")
    if all_gpus["launcher"] != "multi_gpu_launcher":
        raise AssertionError("Expected gpu_ids='all' to take the multi-GPU path.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
