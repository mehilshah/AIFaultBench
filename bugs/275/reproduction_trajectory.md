# Reproduction Trajectory — Bug 275: detectron2

- **Bug report:** [https://github.com/facebookresearch/detectron2/issues/4915](https://github.com/facebookresearch/detectron2/issues/4915)
- **Repository:** facebookresearch/detectron2 @ `1f84ebbf5af96eae71e2c0476d49e9cbdc5b190f`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run setup_env.sh to create or reuse the local virtualenv and install the pinned runtime dependencies.
2. Export PYTHONPATH to include the local codebase/ tree.
3. Execute repro.py, which builds the local Mask R-CNN config, scripts it with scripting_with_instances(), and fails during torch.jit.save().

## Observed behavior

- On torch 2.5.1+cpu, torch.jit.save(scripted_model) fails with RuntimeError: Could not export Python function call 'is_fx_tracing'. The traceback points to codebase/detectron2/modeling/poolers.py:223 inside ROIPooler.forward.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
