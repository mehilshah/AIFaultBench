#!/usr/bin/env python3
"""Reproduce the TPU config validation AttributeError from accelerate."""

from __future__ import annotations

import importlib.util
import json
import sys
import traceback
import types
from argparse import Namespace
from enum import Enum
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE_SRC = ROOT / "codebase" / "src"
CONFIG_FILE = ROOT / "tpu_config.yaml"
RESULT_FILE = ROOT / "reproduction.json"


def install_stubs() -> None:
    """Install minimal module stubs so the launcher can be imported without the local torch build."""
    torch = types.ModuleType("torch")
    torch.__version__ = "stub"
    torch.device = lambda *args, **kwargs: ("device", args, kwargs)
    torch.cuda = types.SimpleNamespace(
        is_available=lambda: False,
        device_count=lambda: 0,
        set_device=lambda device: None,
        get_device_capability=lambda: (0, 0),
        empty_cache=lambda: None,
    )
    torch.distributed = types.SimpleNamespace(
        is_initialized=lambda: False,
        init_process_group=lambda *args, **kwargs: None,
        get_world_size=lambda: 1,
        get_rank=lambda: 0,
        is_mpi_available=lambda: False,
        barrier=lambda: None,
    )
    torch.backends = types.SimpleNamespace(cuda=types.SimpleNamespace(matmul=types.SimpleNamespace(allow_tf32=False)))
    sys.modules["torch"] = torch
    sys.modules["psutil"] = types.ModuleType("psutil")

    accelerate = types.ModuleType("accelerate")
    accelerate.__path__ = [str(CODEBASE_SRC / "accelerate")]
    sys.modules["accelerate"] = accelerate

    commands = types.ModuleType("accelerate.commands")
    commands.__path__ = [str(CODEBASE_SRC / "accelerate" / "commands")]
    sys.modules["accelerate.commands"] = commands

    config_pkg = types.ModuleType("accelerate.commands.config")
    config_pkg.__path__ = [str(CODEBASE_SRC / "accelerate" / "commands" / "config")]
    sys.modules["accelerate.commands.config"] = config_pkg

    utils = types.ModuleType("accelerate.utils")

    class ComputeEnvironment(str, Enum):
        LOCAL_MACHINE = "LOCAL_MACHINE"
        AMAZON_SAGEMAKER = "AMAZON_SAGEMAKER"

    class DistributedType(str, Enum):
        DEEPSPEED = "DEEPSPEED"
        MULTI_GPU = "MULTI_GPU"
        TPU = "TPU"
        FSDP = "FSDP"
        MPS = "MPS"
        MEGATRON_LM = "MEGATRON_LM"

    class SageMakerDistributedType(str, Enum):
        NO = "NO"
        DATA_PARALLEL = "DATA_PARALLEL"
        MODEL_PARALLEL = "MODEL_PARALLEL"

    utils.ComputeEnvironment = ComputeEnvironment
    utils.DistributedType = DistributedType
    utils.SageMakerDistributedType = SageMakerDistributedType
    utils.PrepareForLaunch = object
    utils._filter_args = lambda *args, **kwargs: []
    utils.is_deepspeed_available = lambda: False
    utils.is_rich_available = lambda: False
    utils.is_sagemaker_available = lambda: False
    utils.is_torch_version = lambda *args, **kwargs: True
    utils.patch_environment = lambda *args, **kwargs: None
    utils.prepare_deepspeed_cmd_env = lambda *args, **kwargs: ({}, [])
    utils.prepare_multi_gpu_env = lambda *args, **kwargs: ({}, [])
    utils.prepare_sagemager_args_inputs = lambda *args, **kwargs: ({}, {})
    utils.prepare_simple_launcher_cmd_env = lambda *args, **kwargs: ({}, [])
    utils.prepare_tpu = lambda *args, **kwargs: ({}, [])
    sys.modules["accelerate.utils"] = utils

    utils_constants = types.ModuleType("accelerate.utils.constants")
    utils_constants.SAGEMAKER_PYTORCH_VERSION = "1.10.2"
    utils_constants.SAGEMAKER_PYTHON_VERSION = "py38"
    utils_constants.SAGEMAKER_TRANSFORMERS_VERSION = "4.17.0"
    utils_constants.DEEPSPEED_MULTINODE_LAUNCHERS = ["pdsh", "standard"]
    utils_constants.TORCH_DYNAMO_MODES = ["default", "reduce-overhead", "max-autotune"]
    sys.modules["accelerate.utils.constants"] = utils_constants

    state = types.ModuleType("accelerate.state")
    state.get_int_from_env = lambda *args, **kwargs: 0
    sys.modules["accelerate.state"] = state

    config_utils = types.ModuleType("accelerate.commands.config.config_utils")
    config_utils.DYNAMO_BACKENDS = ["EAGER", "AOT_EAGER"]
    sys.modules["accelerate.commands.config.config_utils"] = config_utils


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


def build_args(config_file: Path) -> Namespace:
    return Namespace(
        multi_gpu=False,
        cpu=False,
        tpu=False,
        tpu_cluster=False,
        mps=False,
        use_deepspeed=False,
        use_fsdp=False,
        use_megatron_lm=False,
        config_file=str(config_file),
        gpu_ids=None,
        num_machines=None,
        mixed_precision=None,
        dynamo_backend=None,
    )


def write_result(reproducible: bool, evidence: str, steps: list[str], blocking_reason: str) -> None:
    payload = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": steps,
        "blocking_reason": blocking_reason,
        "reproduction_command": "bash run_repro.sh",
    }
    RESULT_FILE.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    install_stubs()

    config_args = load_module(
        "accelerate.commands.config.config_args",
        CODEBASE_SRC / "accelerate" / "commands" / "config" / "config_args.py",
    )
    config_pkg = sys.modules["accelerate.commands.config"]
    config_pkg.default_config_file = config_args.default_config_file
    config_pkg.load_config_from_file = config_args.load_config_from_file
    config_pkg.ClusterConfig = config_args.ClusterConfig

    launch = load_module(
        "accelerate.commands.launch",
        CODEBASE_SRC / "accelerate" / "commands" / "launch.py",
    )

    try:
        launch._validate_launch_command(build_args(CONFIG_FILE))
    except Exception as exc:
        traceback.print_exc()
        target = isinstance(exc, AttributeError) and "ClusterConfig" in str(exc) and "tpu_cluster" in str(exc)
        if target:
            print("reproduced: accelerate.commands.launch._validate_launch_command raises AttributeError on tpu_cluster")
            write_result(
                True,
                "AttributeError at codebase/src/accelerate/commands/launch.py:793: 'ClusterConfig' object has no attribute 'tpu_cluster'.",
                [
                    "Install the minimal dependency set.",
                    "Load the real launcher from codebase/src/accelerate/commands/launch.py with TPU config defaults.",
                    "Call _validate_launch_command; it dereferences defaults.tpu_cluster and raises AttributeError.",
                ],
                "",
            )
            return 0

        print("unexpected exception type; see stderr for the traceback")
        write_result(
            False,
            f"Unexpected exception while reproducing the bug: {type(exc).__name__}: {exc}",
            [
                "Install the minimal dependency set.",
                "Load the launcher harness.",
                "Encountered an unexpected exception before the target AttributeError.",
            ],
            f"Unexpected exception: {type(exc).__name__}: {exc}",
        )
        return 1

    print("no exception raised; the bug did not reproduce")
    write_result(
        False,
        "The launcher returned successfully instead of raising the expected AttributeError.",
        [
            "Install the minimal dependency set.",
            "Load the launcher harness.",
            "Run _validate_launch_command with TPU defaults.",
        ],
        "The launcher completed without error.",
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
