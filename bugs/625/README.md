# Bug 625

This folder contains a minimal reproduction bundle for DeepSpeed issue #7708.

What the repro does:
- imports the local `codebase/`
- constructs a minimal `DeepSpeedEngine` object without running full training
- invokes the real backward hook path with `grad=None`
- reproduces the `TypeError` from `DeepSpeedEngine._backward_prologue_per_tensor`

Relevant source locations:
- [`codebase/deepspeed/runtime/engine.py`](./codebase/deepspeed/runtime/engine.py)
- [`codebase/deepspeed/runtime/utils.py`](./codebase/deepspeed/runtime/utils.py)

How to run:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

The run writes stdout to `repro_stdout.log` and stderr to `repro_stderr.log`.
