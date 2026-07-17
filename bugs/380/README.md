# DeepSpeed ZeRO-2 Hook-Count Regression Repro

This folder reproduces DeepSpeed issue [#7885](https://github.com/deepspeedai/DeepSpeed/issues/7885).

## What the repro checks

The regression is in the ZeRO-2 backward hook path:

- `0.18.4` refreshes the expected hook count once per backward pass.
- `0.18.5` refreshes it once per parameter hook, which scales with the number of tensors and slows training.

The bundled benchmark uses a small CPU ZeRO-2 workload so it can run without relying on a specific GPU architecture.

## Files

- `setup_env.sh`: creates the dependency directory and installs the base runtime dependencies.
- `run_repro.sh`: creates the dependency directory, installs DeepSpeed `0.18.4` and `0.18.5`, runs the benchmark twice, and writes `reproduction.json`.
- `repro.py`: the benchmark itself.
- `requirements.txt`: base Python dependencies for the repro environment.

## Expected outcome

When the bug is present, `0.18.5` shows many more `count_used_parameters_in_backward()` calls and a noticeably slower step time than `0.18.4`.

Run:

```bash
bash run_repro.sh
```
