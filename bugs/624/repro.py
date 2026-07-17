#!/usr/bin/env python3
"""Reproduce accelerate issue 903: invalid launch args are accepted."""

from __future__ import annotations

import argparse
import enum
import importlib.util
import logging
import sys
import types
from contextlib import contextmanager
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE_SRC = ROOT / "codebase" / "src"
LAUNCH_PATH = CODEBASE_SRC / "accelerate" / "commands" / "launch.py"


def register_module(name: str, *, is_package: bool = False):
    module = types.ModuleType(name)
    if is_package:
        module.__path__ = []  # type: ignore[attr-defined]
    sys.modules[name] = module
    return module


def install_runtime_stubs():
    """Keep the repro independent from the broken global torch installation."""
    torch = register_module("torch", is_package=True)

    class _Cuda:
        @staticmethod
        def device_count():
            return 8

        @staticmethod
        def is_available():
            return True

        @staticmethod
        def is_bf16_supported():
            return False

    torch.cuda = _Cuda()
    torch.__version__ = "2.5.1"

    psutil = register_module("psutil")
    psutil.cpu_count = lambda logical=False: 16

    # Create a minimal accelerate package surface so launch.py can load without
    # importing the full library and its heavy torch-dependent modules.
    accel = register_module("accelerate", is_package=True)
    accel.__path__ = [str(CODEBASE_SRC / "accelerate")]  # type: ignore[attr-defined]

    commands = register_module("accelerate.commands", is_package=True)
    commands.__path__ = [str(CODEBASE_SRC / "accelerate" / "commands")]  # type: ignore[attr-defined]

    config_pkg = register_module("accelerate.commands.config", is_package=True)
    config_pkg.default_config_file = str(ROOT / "nonexistent_default_config.yaml")
    config_pkg.load_config_from_file = lambda config_file: None

    config_args = register_module("accelerate.commands.config.config_args")

    class SageMakerConfig:
        pass

    config_args.SageMakerConfig = SageMakerConfig

    config_utils = register_module("accelerate.commands.config.config_utils")
    config_utils.DYNAMO_BACKENDS = ["EAGER"]

    state_mod = register_module("accelerate.state")
    state_mod.get_int_from_env = lambda names, default=1: default

    utils_pkg = register_module("accelerate.utils", is_package=True)

    class ComputeEnvironment(enum.Enum):
        LOCAL_MACHINE = "LOCAL_MACHINE"
        AMAZON_SAGEMAKER = "AMAZON_SAGEMAKER"

    class DistributedType(enum.Enum):
        NO = "NO"
        MULTI_GPU = "MULTI_GPU"
        DEEPSPEED = "DEEPSPEED"
        FSDP = "FSDP"
        TPU = "TPU"
        MPS = "MPS"
        MEGATRON_LM = "MEGATRON_LM"

    class DynamoBackend(enum.Enum):
        NO = "NO"
        EAGER = "EAGER"

    class PrecisionType(enum.Enum):
        NO = "no"
        FP16 = "fp16"
        BF16 = "bf16"

        @classmethod
        def list(cls):
            return [item.value for item in cls]

    class PrepareForLaunch:
        def __init__(self, launcher, distributed_type="NO", debug=False):
            self.launcher = launcher

        def __call__(self, *args, **kwargs):
            return self.launcher(*args, **kwargs)

    def _filter_args(args):
        return args

    def is_deepspeed_available():
        return False

    def is_rich_available():
        return False

    def is_sagemaker_available():
        return False

    def is_torch_version(*args, **kwargs):
        return True

    @contextmanager
    def patch_environment(**kwargs):
        yield

    utils_pkg.ComputeEnvironment = ComputeEnvironment
    utils_pkg.DistributedType = DistributedType
    utils_pkg.DynamoBackend = DynamoBackend
    utils_pkg.PrecisionType = PrecisionType
    utils_pkg.PrepareForLaunch = PrepareForLaunch
    utils_pkg._filter_args = _filter_args
    utils_pkg.is_deepspeed_available = is_deepspeed_available
    utils_pkg.is_rich_available = is_rich_available
    utils_pkg.is_sagemaker_available = is_sagemaker_available
    utils_pkg.is_torch_version = is_torch_version
    utils_pkg.patch_environment = patch_environment

    constants_mod = register_module("accelerate.utils.constants")
    constants_mod.DEEPSPEED_MULTINODE_LAUNCHERS = ["pdsh", "standard", "openmpi", "mvapich"]

    dataclasses_mod = register_module("accelerate.utils.dataclasses")
    dataclasses_mod.SageMakerDistributedType = DistributedType

    launch_mod = register_module("accelerate.utils.launch")
    launch_mod.env_var_path_add = lambda env_var_name, path_to_add: f"{env_var_name}:{path_to_add}"

    return torch


def load_launch_module():
    spec = importlib.util.spec_from_file_location("accelerate.commands.launch", LAUNCH_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["accelerate.commands.launch"] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main():
    install_runtime_stubs()
    launch = load_launch_module()

    seen = {}

    def fake_multi_gpu_launcher(args):
        seen["launcher"] = "multi_gpu"

    def fake_simple_launcher(args):
        seen["launcher"] = "simple"

    launch.multi_gpu_launcher = fake_multi_gpu_launcher
    launch.simple_launcher = fake_simple_launcher

    argv = [
        "--multi_gpu",
        "--gpu_ids",
        "0,1,2,3",
        "--mixed_precision",
        "no",
        "--num_machines",
        "1",
        "--num_processes",
        "1",
        "--num_cpu_threads_per_process=1",
        "dummy.py",
    ]
    args = launch.launch_command_parser().parse_args(argv)

    try:
        launch.launch_command(args)
    except Exception as exc:  # pragma: no cover - this path would refute the bug
        print(f"unexpected_exception={type(exc).__name__}: {exc}")
        raise

    print("accepted_invalid_combo=True")
    print(f"launcher_called={seen.get('launcher')}")
    print(f"multi_gpu_flag={args.multi_gpu}")
    print(f"num_processes={args.num_processes}")
    print(f"num_machines={args.num_machines}")

    if seen.get("launcher") == "multi_gpu" and args.multi_gpu and args.num_processes == 1:
        print("evidence=launch_command dispatched the invalid combination to multi_gpu_launcher")
    else:
        print("evidence=bug_not_reproduced")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
