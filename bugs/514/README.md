# Bug 514

This bundle reproduces the DeepCompile profiling failure described in `bug_report.txt`.

The relevant DeepSpeed code path is the FX profiling interpreter in:
- [`codebase/deepspeed/compile/profilers/graph_profile.py`](codebase/deepspeed/compile/profilers/graph_profile.py#L77)
- [`codebase/deepspeed/compile/passes/zero3_compile.py`](codebase/deepspeed/compile/passes/zero3_compile.py#L151)

What the repro does:
- Builds the backward graph for `torch.nn.functional.cross_entropy` with `torch.func.grad`.
- Forces the same decomposed chain that appears in the issue report, including `full_like` and `scatter`.
- Runs the graph under a lowered virtual-memory cap to emulate the fixed memory budget that triggers the profiling OOM.

Observed result in this folder:
- Eager `cross_entropy` succeeds.
- The decomposed FX graph fails with `RuntimeError: DefaultCPUAllocator: can't allocate memory`.

How to run:
1. `./setup_env.sh`
2. `./run_repro.sh`

The repro is CPU-only because the local environment does not provide a working CUDA-enabled PyTorch installation.
