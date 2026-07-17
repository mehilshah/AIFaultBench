# Reproduction Trajectory — Bug 486: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/1200](https://github.com/huggingface/accelerate/issues/1200)
- **Repository:** huggingface/accelerate @ `e4620984f8f2d3b91585f7d8c03f8c57cd453f50`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created an isolated venv with torch 2.2.2+cpu, numpy<2, setuptools<81, and the local accelerate checkout installed editable.
2. Ran the report's minimal scheduler snippet through `repro.py`.
3. Observed that `accelerator.prepare(...)` returned `AcceleratedScheduler` and `hasattr(scheduler, "scheduler")` was true.

## Observed behavior

- Final repro output: {"accelerate_scheduler_type": "AcceleratedScheduler", "has_scheduler_attr": true, "is_accelerated_scheduler": true, "python_version": "3.12.3", "torch_version": "2.2.2+cpu"}
- The captured run also shows no application error; only a non-fatal pkg_resources deprecation warning remained in stderr.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```

## Why it does not reproduce on the reference machine

This checkout is already on the post-fix scheduler-import path, and the local host is Python 3.12 rather than the report's Python 3.8 trigger environment. The reported False result does not occur here.
