#!/usr/bin/env python3
"""Reproduce the DecoupledCheckpointEngine hang when the checkpoint process dies."""

from __future__ import annotations

import importlib
import os
import sys
import tempfile
import threading
import time
import types
import multiprocessing as real_mp
from dataclasses import dataclass


ROOT = os.path.dirname(os.path.abspath(__file__))
CODEBASE = os.path.join(ROOT, "codebase")


def _install_package(name: str, path: str) -> types.ModuleType:
    mod = types.ModuleType(name)
    mod.__path__ = [path]
    sys.modules[name] = mod
    return mod


def _install_stubs() -> None:
    # Minimal torch stub: the target module imports torch and torch.multiprocessing,
    # but this repro only needs multiprocessing semantics and a dummy load().
    torch_mod = types.ModuleType("torch")
    torch_mp_mod = types.ModuleType("torch.multiprocessing")

    def get_start_methods(allow_None: bool = False):
        return list(real_mp.get_all_start_methods())

    torch_mp_mod.Process = real_mp.Process
    torch_mp_mod.Event = real_mp.Event
    torch_mp_mod.SimpleQueue = real_mp.SimpleQueue
    torch_mp_mod.get_start_methods = get_start_methods
    torch_mp_mod.set_start_method = real_mp.set_start_method
    torch_mod.multiprocessing = torch_mp_mod
    torch_mod.load = lambda *args, **kwargs: {}
    sys.modules["torch"] = torch_mod
    sys.modules["torch.multiprocessing"] = torch_mp_mod

    # DeepSpeed package stubs. We point package paths at the local codebase so the
    # real checkpoint_engine.py and decoupled_checkpoint_engine.py files are imported.
    _install_package("deepspeed", os.path.join(CODEBASE, "deepspeed"))
    _install_package("deepspeed.runtime", os.path.join(CODEBASE, "deepspeed", "runtime"))
    _install_package(
        "deepspeed.runtime.checkpoint_engine",
        os.path.join(CODEBASE, "deepspeed", "runtime", "checkpoint_engine"),
    )

    comm_mod = types.ModuleType("deepspeed.comm")
    comm_mod.get_rank = lambda: 0
    comm_mod.barrier = lambda: None
    sys.modules["deepspeed.comm"] = comm_mod

    runtime_utils_mod = types.ModuleType("deepspeed.runtime.utils")
    runtime_utils_mod.get_checkpoint_folder_size = lambda save_dir, tag, local_rank: 0
    sys.modules["deepspeed.runtime.utils"] = runtime_utils_mod

    fast_ckpt_mod = types.ModuleType("deepspeed.runtime.checkpoint_engine.fast_checkpoint_engine")

    class FastCheckpointEngine:
        def __init__(self, config_params, dp_writer_config, optimize_dp_state):
            self.config_params = config_params
            self.dp_writer_config = dp_writer_config
            self.optimize_dp_state = optimize_dp_state

        def save(self, state_dict, save_path):
            # The real repro only needs the child process to exist and be killable.
            return None

    fast_ckpt_mod.FastCheckpointEngine = FastCheckpointEngine
    sys.modules["deepspeed.runtime.checkpoint_engine.fast_checkpoint_engine"] = fast_ckpt_mod


@dataclass
class DummyWriterConfig:
    local_rank: int = 0


def _load_target_module():
    # Import the real module code from the local snapshot after the stubbed
    # dependencies have been installed.
    return importlib.import_module("deepspeed.runtime.checkpoint_engine.decoupled_checkpoint_engine")


def reproduce_hang() -> bool:
    module = _load_target_module()
    DecoupledCheckpointEngine = module.DecoupledCheckpointEngine
    CheckpointCommitInfo = module.CheckpointCommitInfo

    with tempfile.TemporaryDirectory(prefix="ds-decoupled-hang-") as tmpdir:
        engine = DecoupledCheckpointEngine({}, DummyWriterConfig(), False)
        info = CheckpointCommitInfo(tag="step-1", save_dir=tmpdir, save_latest=False)
        engine.create(info)

        child_pid = engine.ckpt_process.pid
        print(f"checkpoint child started: pid={child_pid}")
        engine.ckpt_process.terminate()
        engine.ckpt_process.join(timeout=5)
        print(f"checkpoint child alive after terminate: {engine.ckpt_process.is_alive()}")

        outcome = {"returned": False, "exception": None}

        def call_commit():
            try:
                outcome["returned"] = engine.commit(info)
            except BaseException as exc:  # pragma: no cover - defensive capture for debugging
                outcome["exception"] = repr(exc)

        t = threading.Thread(target=call_commit, daemon=True)
        t.start()
        t.join(timeout=2)

        if t.is_alive():
            print("commit() is still blocked after 2s")
            print("evidence: save_event.wait() does not time out and there is no process-health check")
            print("result: reproducible")
            if engine.ckpt_process.is_alive():
                engine.ckpt_process.terminate()
            engine.ckpt_process.join(timeout=5)
            return True

        print(f"commit() returned unexpectedly: {outcome}")
        return False


def main() -> int:
    _install_stubs()
    reproduced = reproduce_hang()
    return 0 if reproduced else 1


if __name__ == "__main__":
    raise SystemExit(main())
