#!/usr/bin/env python3
"""Reproduce the Accelerate CLI rendezvous-backend mismatch from issue #1489."""

from __future__ import annotations

import json
import sys
import tempfile
from contextlib import suppress
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE_SRC = ROOT / "codebase" / "src"
if str(CODEBASE_SRC) not in sys.path:
    sys.path.insert(0, str(CODEBASE_SRC))


def _load_accelerate():
    from accelerate.commands.config.config_args import load_config_from_file
    from accelerate.commands.launch import launch_command, launch_command_parser

    return load_config_from_file, launch_command, launch_command_parser


def _capture_launch(cli_args: list[str]) -> dict[str, object]:
    """Run the launch path without starting distributed workers."""
    import torch.distributed.run as distrib_run

    _, launch_command, launch_command_parser = _load_accelerate()

    captured: dict[str, object] = {}
    original_run = distrib_run.run

    def fake_run(args):
        captured["rdzv_backend"] = getattr(args, "rdzv_backend", None)
        captured["rdzv_endpoint"] = getattr(args, "rdzv_endpoint", None)
        captured["nnodes"] = getattr(args, "nnodes", None)
        captured["nproc_per_node"] = getattr(args, "nproc_per_node", None)
        captured["node_rank"] = getattr(args, "node_rank", None)
        captured["training_script"] = getattr(args, "training_script", None)
        captured["training_script_args"] = getattr(args, "training_script_args", None)
        raise RuntimeError("__CAPTURED__")

    distrib_run.run = fake_run
    try:
        parser = launch_command_parser()
        parsed = parser.parse_args(cli_args)
        captured["parsed_has_rdzv_backend_attr"] = hasattr(parsed, "rdzv_backend")
        with suppress(RuntimeError):
            launch_command(parsed)
    finally:
        distrib_run.run = original_run

    return captured


def _yaml_roundtrip() -> dict[str, object]:
    load_config_from_file, _, _ = _load_accelerate()
    config_text = """\
compute_environment: LOCAL_MACHINE
distributed_type: MULTI_GPU
mixed_precision: no
use_cpu: false
num_processes: 8
num_machines: 2
machine_rank: 0
main_process_ip: 10.13.23.78
main_process_port: 7010
rdzv_backend: c10d
same_network: false
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "accelerate_config.yaml"
        config_path.write_text(config_text, encoding="utf-8")
        cfg = load_config_from_file(str(config_path))
        return {
            "loaded_type": type(cfg).__name__,
            "yaml_rdzv_backend": getattr(cfg, "rdzv_backend", None),
            "yaml_same_network": getattr(cfg, "same_network", None),
            "yaml_main_process_ip": getattr(cfg, "main_process_ip", None),
            "yaml_main_process_port": getattr(cfg, "main_process_port", None),
        }


def main() -> int:
    _, _, launch_command_parser = _load_accelerate()

    parser = launch_command_parser()
    cli_help = parser.format_help()
    accepts_rdzv_backend = "--rdzv_backend" in cli_help

    cli_args = [
        "--main_process_ip",
        "10.13.23.78",
        "--main_process_port",
        "7010",
        "--multi_gpu",
        "--mixed_precision=no",
        "--num_processes=8",
        "--dynamo_backend=no",
        "--num_machines=2",
        "--machine_rank=0",
        "--rdzv_conf",
        "rdzv_endpoint=10.13.23.78:7010,rdzv_backend=c10d",
        str(ROOT / "repro_worker.py"),
    ]
    captured = _capture_launch(cli_args)
    yaml_info = _yaml_roundtrip()

    result = {
        "cli_accepts_rdzv_backend_flag": accepts_rdzv_backend,
        "cli_effective_rdzv_backend": captured.get("rdzv_backend"),
        "cli_effective_rdzv_endpoint": captured.get("rdzv_endpoint"),
        "cli_effective_nnodes": captured.get("nnodes"),
        "cli_effective_nproc_per_node": captured.get("nproc_per_node"),
        "cli_effective_node_rank": captured.get("node_rank"),
        "yaml_info": yaml_info,
    }

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
