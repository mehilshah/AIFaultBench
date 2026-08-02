#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import logging
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"

import torch


def _install_deepspeed_stubs() -> types.ModuleType:
    """Load the target DeepSpeed source file without importing the full package tree."""

    def module(name: str, **attrs):
        mod = types.ModuleType(name)
        for key, value in attrs.items():
            setattr(mod, key, value)
        return mod

    class _NullContext:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    class DummyAccelerator:
        def device_name(self, device_index=None):
            return "cpu"

        def current_device_name(self):
            return "cpu"

        def device(self, device_index=None):
            return torch.device("cpu")

        def memory_reserved(self, device_index=None):
            return 0

        def max_memory_reserved(self, device_index=None):
            return 0

        def memory_allocated(self, device_index=None):
            return 0

        def max_memory_allocated(self, device_index=None):
            return 0

        def memory_cached(self, device_index=None):
            return 0

        def max_memory_cached(self, device_index=None):
            return 0

        def synchronize(self, device_index=None):
            return None

        def FloatTensor(self, data):
            return torch.tensor(data, dtype=torch.float32)

        def ByteTensor(self, data):
            return torch.tensor(data, dtype=torch.uint8)

        def current_stream(self, device_index=None):
            return None

        def stream(self, stream):
            return _NullContext()

        def Stream(self):
            return None

        def create_graph(self):
            return None

        def capture_to_graph(self, graph):
            return _NullContext()

        def replay_graph(self, graph):
            return None

    ds_pkg = module("deepspeed")
    ds_pkg.__path__ = [str(CODEBASE / "deepspeed")]
    sys.modules["deepspeed"] = ds_pkg

    sys.modules["deepspeed.comm"] = module("deepspeed.comm")
    sys.modules["deepspeed.moe"] = module("deepspeed.moe")
    sys.modules["deepspeed.moe.utils"] = module("deepspeed.moe.utils", is_moe_param=lambda *args, **kwargs: False)
    sys.modules["deepspeed.utils"] = module(
        "deepspeed.utils",
        groups=types.SimpleNamespace(),
        logger=logging.getLogger("deepspeed"),
    )
    sys.modules["deepspeed.utils.bwc"] = module(
        "deepspeed.utils.bwc",
        bwc_tensor_model_parallel_rank=lambda *args, **kwargs: 0,
        bwc_pipeline_parallel_world_size=lambda *args, **kwargs: 0,
        bwc_pipeline_parallel_group=lambda *args, **kwargs: None,
    )
    sys.modules["deepspeed.runtime"] = module("deepspeed.runtime")
    sys.modules["deepspeed.runtime.constants"] = module("deepspeed.runtime.constants", PIPE_REPLICATED=None)
    sys.modules["deepspeed.accelerator"] = module(
        "deepspeed.accelerator",
        get_accelerator=lambda: DummyAccelerator(),
    )
    sys.modules["deepspeed.module_inject"] = module("deepspeed.module_inject")
    sys.modules["deepspeed.module_inject.policy"] = module(
        "deepspeed.module_inject.policy",
        transpose=lambda value: value,
    )

    spec = importlib.util.spec_from_file_location("deepspeed.runtime.utils", CODEBASE / "deepspeed/runtime/utils.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load DeepSpeed runtime utils from source")
    module_obj = importlib.util.module_from_spec(spec)
    sys.modules["deepspeed.runtime.utils"] = module_obj
    spec.loader.exec_module(module_obj)
    return module_obj


def main() -> None:
    ds_utils = _install_deepspeed_stubs()

    if not hasattr(torch.autograd.graph, "_get_grad_fn_or_grad_acc"):
        raise RuntimeError("torch.autograd.graph._get_grad_fn_or_grad_acc is unavailable")

    original_lookup = torch.autograd.graph._get_grad_fn_or_grad_acc
    lookup_calls = {"count": 0}

    def guarded_lookup(tensor):
        lookup_calls["count"] += 1
        if not torch.is_grad_enabled():
            raise RuntimeError("grad mode must be enabled for grad-acc lookup")
        return original_lookup(tensor)

    torch.autograd.graph._get_grad_fn_or_grad_acc = guarded_lookup

    param = torch.nn.Parameter(torch.tensor([1.0], requires_grad=True))
    seen = {}

    def hook(_grad):
        seen["hook_grad_enabled"] = torch.is_grad_enabled()
        seen["count"] = ds_utils.count_used_parameters_in_backward([param])
        return _grad

    param.register_hook(hook)
    loss = (param * 2.0).sum()
    loss.backward()

    print({"lookup_calls": lookup_calls["count"], "hook_grad_enabled": seen["hook_grad_enabled"], "count": seen["count"]})


if __name__ == "__main__":
    main()
