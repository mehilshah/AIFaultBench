# Bug 612

This folder contains a minimal reproduction for DeepSpeed issue 7710.

Reported failure:
- `IndexError: list index out of range`
- Source location: `codebase/deepspeed/runtime/zero/stage_1_and_2.py`
- Offending access: `bucket.buffer[bucket.index]` inside `reduce_ipg_grads()`

Why this repro is source-level:
- The local environment cannot import the full DeepSpeed package because the installed CUDA-enabled `torch` build fails to load its NCCL symbol dependencies.
- The repro therefore exercises the exact empty-bucket access in a small self-contained harness, which still reproduces the same `IndexError`.

Run:
```bash
./run_repro.sh
```

Artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`
