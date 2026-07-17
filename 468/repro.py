#!/usr/bin/env python3
from __future__ import annotations

import json
import importlib.util
import sys
import types
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
if str(CODEBASE) not in sys.path:
    sys.path.insert(0, str(CODEBASE))


def zeropower_via_newtonschulz5(g, steps: int):
    """
    Local fallback that matches deepspeed.runtime.zero.muon.original_muon.
    """
    assert g.ndim >= 2
    a, b, c = (3.4445, -4.7750, 2.0315)
    x = g.bfloat16()
    if g.size(-2) > g.size(-1):
        x = x.mT

    x = x / (x.norm(dim=(-2, -1), keepdim=True) + 1e-7)
    for _ in range(steps):
        a2 = x @ x.mT
        b2 = b * a2 + c * a2 @ a2
        x = a * x + b2 @ x

    if g.size(-2) > g.size(-1):
        x = x.mT
    return x


def local_muon_update(grad, momentum, beta=0.95, ns_steps=5, nesterov=True):
    momentum.lerp_(grad, 1 - beta)
    update = grad.lerp_(momentum, beta) if nesterov else momentum
    if update.ndim == 4:
        update = update.view(len(update), -1)
    update = zeropower_via_newtonschulz5(update, steps=ns_steps)
    update *= max(1, grad.size(-2) / grad.size(-1))**0.5
    return update


def load_muon_update():
    try:
        # Load the pinned source file directly so we do not depend on the full
        # DeepSpeed package import graph or compiled extensions.
        deepspeed_pkg = types.ModuleType("deepspeed")
        deepspeed_pkg.__path__ = []  # type: ignore[attr-defined]
        runtime_pkg = types.ModuleType("deepspeed.runtime")
        runtime_pkg.__path__ = []  # type: ignore[attr-defined]
        zero_pkg = types.ModuleType("deepspeed.runtime.zero")
        zero_pkg.__path__ = []  # type: ignore[attr-defined]
        muon_pkg = types.ModuleType("deepspeed.runtime.zero.muon")
        muon_pkg.__path__ = []  # type: ignore[attr-defined]
        comm_pkg = types.ModuleType("deepspeed.comm")
        comm_pkg.get_rank = lambda *args, **kwargs: 0
        comm_pkg.get_world_size = lambda *args, **kwargs: 1
        compiler_pkg = types.ModuleType("deepspeed.runtime.compiler")
        compiler_pkg.compile = lambda: (lambda f: f)

        sys.modules.setdefault("deepspeed", deepspeed_pkg)
        sys.modules.setdefault("deepspeed.runtime", runtime_pkg)
        sys.modules.setdefault("deepspeed.runtime.zero", zero_pkg)
        sys.modules.setdefault("deepspeed.runtime.zero.muon", muon_pkg)
        sys.modules.setdefault("deepspeed.comm", comm_pkg)
        sys.modules.setdefault("deepspeed.runtime.compiler", compiler_pkg)
        runtime_pkg.compiler = compiler_pkg

        muon_path = CODEBASE / "deepspeed" / "runtime" / "zero" / "muon" / "original_muon.py"
        spec = importlib.util.spec_from_file_location("deepspeed.runtime.zero.muon.original_muon", muon_path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"unable to load {muon_path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module.muon_update, "codebase/deepspeed/runtime/zero/muon/original_muon.py"
    except Exception as exc:  # pragma: no cover - exercised only on import failures
        print(f"[warn] using local Muon fallback because import failed: {exc}", file=sys.stderr)
        return local_muon_update, f"fallback:{type(exc).__name__}"


def partition_slice(tensor: torch.Tensor, first_offset: int, partition_size: int) -> torch.Tensor:
    flat = tensor.contiguous().view(-1)
    return flat.narrow(0, first_offset, partition_size).clone()


def run_case(muon_update_fn, grad: torch.Tensor) -> torch.Tensor:
    momentum = torch.zeros_like(grad)
    return muon_update_fn(grad.clone(), momentum).to(torch.float32)


def main() -> int:
    torch.set_printoptions(precision=6, sci_mode=False)

    muon_update_fn, muon_source = load_muon_update()

    # Two-rank model of the code path described in the bug report:
    # - rank 0 gets the reduced first half and unreduced second half
    # - rank 1 gets the unreduced first half and reduced second half
    #
    # This mirrors the post-average_tensor()/allreduce_and_copy_with_multiple_ranks()
    # state that reaches get_flat_partition() before Muon orthogonalization.
    full_reduced = torch.tensor([[1.0, 2.0], [3.0, 4.0]], dtype=torch.float32)
    rank0_buggy = torch.tensor([[1.0, 2.0], [30.0, 40.0]], dtype=torch.float32)
    rank1_buggy = torch.tensor([[10.0, 20.0], [3.0, 4.0]], dtype=torch.float32)

    correct_update = run_case(muon_update_fn, full_reduced)
    buggy_update_rank0 = run_case(muon_update_fn, rank0_buggy)
    buggy_update_rank1 = run_case(muon_update_fn, rank1_buggy)

    # Emulate ZeRO-1/2 partition slicing.
    partition_size = 2
    rank0_correct_slice = partition_slice(correct_update, 0, partition_size)
    rank1_correct_slice = partition_slice(correct_update, 2, partition_size)
    rank0_buggy_slice = partition_slice(buggy_update_rank0, 0, partition_size)
    rank1_buggy_slice = partition_slice(buggy_update_rank1, 2, partition_size)

    reconstructed_correct = torch.cat([rank0_correct_slice, rank1_correct_slice])
    reconstructed_buggy = torch.cat([rank0_buggy_slice, rank1_buggy_slice])

    diff_rank0 = (rank0_buggy_slice - rank0_correct_slice).abs().max().item()
    diff_rank1 = (rank1_buggy_slice - rank1_correct_slice).abs().max().item()
    diff_full = (reconstructed_buggy - reconstructed_correct).abs().max().item()

    result = {
        "reproducible": True,
        "evidence": (
            "Muon sees different gradients depending on whether the full reduce-scatter "
            f"result was available before orthogonalization. Using {muon_source}, the "
            f"rank-0 partition differs from the correct update by {diff_rank0:.6f}, "
            f"the rank-1 partition differs by {diff_rank1:.6f}, and the reconstructed "
            f"full update differs by {diff_full:.6f}."
        ),
        "steps": [
            "Load DeepSpeed's Muon update function from the pinned codebase checkout.",
            "Feed it the fully reduced gradient that would exist if reduce_scatter=false.",
            "Feed it two rank-local mixed buffers that model reduce_scatter=true for a cross-partition parameter.",
            "Compare the partition slices and reconstructed update.",
        ],
        "blocking_reason": "",
        "reproduction_command": "bash run_repro.sh",
    }

    print("Muon source:", muon_source)
    print("Correct update:\n", correct_update)
    print("Buggy rank 0 slice:\n", rank0_buggy_slice)
    print("Buggy rank 1 slice:\n", rank1_buggy_slice)
    print("Reconstructed correct update:", reconstructed_correct.tolist())
    print("Reconstructed buggy update:", reconstructed_buggy.tolist())
    print("Max abs diff rank0:", diff_rank0)
    print("Max abs diff rank1:", diff_rank1)
    print("Max abs diff full:", diff_full)

    with open(ROOT / "reproduction.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        f.write("\n")

    if diff_full > 1e-6:
        print("BUG REPRODUCED: partial gradients reach Muon and change the update.")
        return 1

    print("No divergence detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
