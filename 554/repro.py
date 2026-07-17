#!/usr/bin/env python3
"""Minimal reproduction for the DistNeighborLoader RPC unpack failure.

The issue report shows a crash in:

    torch_geometric/distributed/rpc.py: rpc_partition_to_workers()

This script keeps the repro local and deterministic by:
1. Loading the vendored PyG modules directly from `codebase/`.
2. Bootstrapping a one-worker RPC runtime so the decorator gate is satisfied.
3. Replacing `global_all_gather` with a result that contains a `None` entry.
4. Calling `rpc_partition_to_workers(...)` and letting the TypeError surface.
"""

from __future__ import annotations

import importlib.util
import pathlib
import socket
import sys
import types


ROOT = pathlib.Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"


def ensure_package(name: str, path: pathlib.Path) -> None:
    module = sys.modules.get(name)
    if module is None:
        module = types.ModuleType(name)
        module.__path__ = [str(path)]
        sys.modules[name] = module


def load_module(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec for {name} at {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    # Keep the vendored package isolated from any globally installed PyG.
    ensure_package("torch_geometric", CODEBASE / "torch_geometric")
    ensure_package("torch_geometric.distributed",
                   CODEBASE / "torch_geometric" / "distributed")

    dist_context_mod = load_module(
        "torch_geometric.distributed.dist_context",
        CODEBASE / "torch_geometric" / "distributed" / "dist_context.py",
    )
    dist_rpc = load_module(
        "torch_geometric.distributed.rpc",
        CODEBASE / "torch_geometric" / "distributed" / "rpc.py",
    )

    from torch.distributed import rpc

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]

    backend_opts = rpc.TensorPipeRpcBackendOptions(
        init_method=f"tcp://127.0.0.1:{port}",
        num_worker_threads=1,
        rpc_timeout=10,
    )
    rpc.init_rpc(
        name="worker0",
        rank=0,
        world_size=1,
        rpc_backend_options=backend_opts,
    )

    ctx = dist_context_mod.DistContext(
        rank=0,
        global_rank=0,
        world_size=1,
        global_world_size=1,
        group_name="dist-loader-test",
    )

    def fake_all_gather(obj, timeout=None):
        # Mimic a missing or desynchronized worker response.
        return {
            "dist-loader-test-0": (ctx.role, 2, 0),
            "dist-loader-test-1": None,
        }

    dist_rpc.global_all_gather = fake_all_gather

    try:
        dist_rpc.rpc_partition_to_workers(ctx, num_partitions=2,
                                          current_partition_idx=0)
    finally:
        rpc.shutdown()


if __name__ == "__main__":
    main()
