#!/usr/bin/env python3
"""Reproduce the FastFileWriter file-descriptor leak.

This loads the DeepSpeed `io` modules directly from `codebase/` so the repro
does not depend on importing the full `deepspeed` package or its optional
runtime dependencies.

The key observation is that `FastFileWriter.close()` calls `_fini()`, and
`_fini()` only overwrites `self._aio_fd` instead of closing the OS file
descriptor. After unlinking each file, the leaked fd remains visible as a
deleted entry under `/proc/<pid>/fd`.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import pathlib
import sys
import types
from dataclasses import dataclass

import torch


ROOT = pathlib.Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
IO_DIR = CODEBASE / "deepspeed" / "io"


def _ensure_package(name: str) -> types.ModuleType:
    module = sys.modules.get(name)
    if module is None:
        module = types.ModuleType(name)
        module.__path__ = []  # mark as package
        sys.modules[name] = module
    return module


def _load_module(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_fast_file_writer():
    _ensure_package("deepspeed")
    _ensure_package("deepspeed.io")
    _ensure_package("deepspeed.ops")
    op_builder_pkg = _ensure_package("deepspeed.ops.op_builder")
    accel_pkg = _ensure_package("deepspeed.accelerator")

    class _FakeUtilsModule:
        def load(self, verbose=True):
            @dataclass
            class _LoadedUtils:
                cast_to_byte_tensor = staticmethod(lambda tensors: tensors)

            return _LoadedUtils()

    class _FakeAccelerator:
        def device_name(self):
            return "cpu"

    op_builder_pkg.UtilsBuilder = _FakeUtilsModule
    accel_pkg.get_accelerator = lambda: _FakeAccelerator()

    _load_module("deepspeed.io.constants", IO_DIR / "constants.py")
    _load_module("deepspeed.io.base_file_writer", IO_DIR / "base_file_writer.py")
    _load_module("deepspeed.io.utils", IO_DIR / "utils.py")
    _load_module("deepspeed.io.base_io_buffer", IO_DIR / "base_io_buffer.py")
    _load_module("deepspeed.io.single_io_buffer", IO_DIR / "single_io_buffer.py")
    _load_module("deepspeed.io.double_io_buffer", IO_DIR / "double_io_buffer.py")
    return _load_module("deepspeed.io.fast_file_writer", IO_DIR / "fast_file_writer.py")


class FakeDnvmeHandle:
    def get_alignment(self):
        return 4096

    def async_pwrite(self, *args, **kwargs):
        raise AssertionError("async_pwrite should not be reached in this repro")

    def wait(self):
        return 1


def count_deleted_fds():
    fd_dir = pathlib.Path(f"/proc/{os.getpid()}/fd")
    deleted = []
    for fd_path in sorted(fd_dir.iterdir(), key=lambda p: int(p.name)):
        try:
            target = os.readlink(fd_path)
        except OSError:
            continue
        if " (deleted)" in target or target.endswith("(deleted)"):
            deleted.append((fd_path.name, target))
    return deleted


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=20)
    parser.add_argument("--workdir", type=pathlib.Path, default=ROOT / "repro_tmp")
    args = parser.parse_args()

    ffw_mod = load_fast_file_writer()
    FastFileWriter = ffw_mod.FastFileWriter
    FastFileWriterConfig = ffw_mod.FastFileWriterConfig

    args.workdir.mkdir(parents=True, exist_ok=True)
    for stale in args.workdir.glob("repro_*.pt"):
        stale.unlink()

    handle = FakeDnvmeHandle()
    pinned_tensor = torch.zeros(4096, dtype=torch.uint8)
    created_paths = []

    for i in range(args.iterations):
        path = args.workdir / f"repro_{i}.pt"
        created_paths.append(path)
        writer = FastFileWriter(
            file_path=str(path),
            config=FastFileWriterConfig(
                dnvme_handle=handle,
                pinned_tensor=pinned_tensor,
                double_buffer=False,
                num_parallel_writers=1,
                writer_rank=0,
                global_rank=0,
            ),
        )
        writer.close()
        os.unlink(path)

    deleted = count_deleted_fds()
    print(f"iterations={args.iterations}")
    print(f"created_files={len(created_paths)}")
    print(f"deleted_fds={len(deleted)}")
    for fd, target in deleted:
        print(f"leaked_fd={fd} target={target}")

    if len(deleted) == args.iterations:
        print("result=bug_reproduced")
    else:
        print("result=bug_not_reproduced")


if __name__ == "__main__":
    main()
