#!/usr/bin/env python3
"""Minimal reproduction for DeepSpeed issue 7711.

This harness loads the real `deepspeed/launcher/multinode_runner.py` source from
the checked-in codebase, but stubs the unrelated DeepSpeed package imports that
would otherwise require a full GPU/MPI environment. The bug is triggered when
`OpenMPIRunner` validates MPI environment variables too early, before `mpirun`
has a chance to set them.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
import traceback
import types
from collections import OrderedDict
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
RESULT_PATH = ROOT / "reproduction.json"
LAUNCHER_ARGS = "-bind-to none -map-by slot --mca pml ob1 --oversubscribe --display-allocation --display-map"
EXPECTED_ERROR = "MPI environment variables are not set"


class _Logger:
    def info(self, *args, **kwargs):
        print(*args)

    def warning(self, *args, **kwargs):
        print(*args)

    def error(self, *args, **kwargs):
        print(*args, file=sys.stderr)

    def debug(self, *args, **kwargs):
        print(*args)


class _DummyAccelerator:
    def export_envs(self):
        return []

    def device_name(self):
        return "cpu"

    def visible_devices_envs(self):
        return ["CUDA_VISIBLE_DEVICES"]

    def set_visible_devices_envs(self, env, ids):
        return None


def _install_package_stubs() -> None:
    """Install the smallest set of modules needed to import the launcher file."""

    deepspeed_pkg = types.ModuleType("deepspeed")
    deepspeed_pkg.__path__ = [str(CODEBASE / "deepspeed")]

    launcher_pkg = types.ModuleType("deepspeed.launcher")
    launcher_pkg.__path__ = [str(CODEBASE / "deepspeed" / "launcher")]

    accelerator_pkg = types.ModuleType("deepspeed.accelerator")
    accelerator_pkg.get_accelerator = lambda: _DummyAccelerator()

    utils_pkg = types.ModuleType("deepspeed.utils")
    utils_pkg.logger = _Logger()
    utils_pkg.get_numactl_cmd = lambda *args, **kwargs: []
    utils_pkg.set_log_level_from_string = lambda *args, **kwargs: None

    sys.modules.update(
        {
            "deepspeed": deepspeed_pkg,
            "deepspeed.launcher": launcher_pkg,
            "deepspeed.accelerator": accelerator_pkg,
            "deepspeed.utils": utils_pkg,
        }
    )


def _load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _make_args(hostfile: str) -> SimpleNamespace:
    return SimpleNamespace(
        hostfile=hostfile,
        include="",
        exclude="",
        num_nodes=-1,
        num_gpus=-1,
        master_addr="127.0.0.1",
        master_port=29500,
        launcher="openmpi",
        launcher_args=LAUNCHER_ARGS,
        module=False,
        no_python=False,
        no_local_rank=False,
        no_ssh=True,
        no_ssh_check=True,
        force_multi=True,
        user_script="test.py",
        user_args=[],
        save_pid=False,
        enable_each_rank_log="None",
        elastic_training=False,
        max_elastic_nodes=-1,
        min_elastic_nodes=-1,
        ssh_port=None,
        venv_script=None,
        log_level="info",
        quiet=False,
    )


def main() -> int:
    _install_package_stubs()

    # Load the real launcher constants and multinode runner from the codebase.
    _load_module("deepspeed.launcher.constants", CODEBASE / "deepspeed" / "launcher" / "constants.py")
    multinode_runner = _load_module(
        "deepspeed.launcher.multinode_runner", CODEBASE / "deepspeed" / "launcher" / "multinode_runner.py"
    )

    # The issue is triggered before mpirun starts, so a tiny two-node hostfile is enough.
    with tempfile.TemporaryDirectory(prefix="ds599-") as tmpdir:
        hostfile = Path(tmpdir) / "hostfile"
        hostfile.write_text("node-0 slots=1\nnode-1 slots=1\n", encoding="utf-8")

        args = _make_args(str(hostfile))
        resource_pool = OrderedDict([("node-0", 1), ("node-1", 1)])
        world_info_base64 = "unused"

        for key in [
            "OMPI_COMM_WORLD_LOCAL_RANK",
            "OMPI_COMM_WORLD_RANK",
            "OMPI_COMM_WORLD_SIZE",
            "LOCAL_RANK",
            "RANK",
            "WORLD_SIZE",
        ]:
            os.environ.pop(key, None)

        result = {
            "reproducible": False,
            "evidence": "",
            "steps": [
                "Load the real DeepSpeed launcher source from codebase/deepspeed/launcher/multinode_runner.py.",
                "Construct an OpenMPIRunner with a two-host resource pool and no OMPI_* variables in the environment.",
                "Observe the constructor raise OSError: MPI environment variables are not set.",
            ],
            "blocking_reason": "",
            "reproduction_command": "bash run_repro.sh",
        }

        try:
            multinode_runner.OpenMPIRunner(args, world_info_base64, resource_pool)
            result["blocking_reason"] = (
                "OpenMPIRunner instantiated successfully; the expected MPI-environment failure did not occur."
            )
        except Exception as exc:  # noqa: BLE001 - repro harness needs the exact exception type/message
            traceback.print_exc()
            if isinstance(exc, OSError) and EXPECTED_ERROR in str(exc):
                result["reproducible"] = True
                result["evidence"] = (
                    "OpenMPIRunner raised OSError before mpirun launch: "
                    f"{exc.__class__.__name__}: {exc}"
                )
            else:
                result["blocking_reason"] = f"Unexpected exception type or message: {exc.__class__.__name__}: {exc}"

        RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2))

        return 0


if __name__ == "__main__":
    raise SystemExit(main())
