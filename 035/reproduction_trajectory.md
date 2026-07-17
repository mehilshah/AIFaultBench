# Reproduction Trajectory — Bug 035: annotated_deep_learning_paper_implementations

- **Bug report:** [https://github.com/labmlai/annotated_deep_learning_paper_implementations/issues/256](https://github.com/labmlai/annotated_deep_learning_paper_implementations/issues/256)
- **Repository:** labmlai/annotated_deep_learning_paper_implementations @ `999f2036a5a7c54403352211b5d1cc0df42b83f6`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create and activate the local virtual environment via `bash setup_env.sh`.
2. Run `bash run_repro.sh` to execute `repro.py` against the local `codebase/` checkout.
3. Observe the PyTorch size-mismatch RuntimeError when the example uses `RotaryPositionalEmbeddings(3)` with a 4-feature input tensor.

## Observed behavior

- Running the bundle entrypoint reproduces the failure. `bash run_repro.sh` prints `input_shape=(3, 1, 1, 4)` and `rotary_d=3`, then fails with `RuntimeError: The size of tensor a (3) must match the size of tensor b (4) at non-singleton dimension 3` from `labml_nn/transformers/rope/__init__.py:188`. A control run with `RotaryPositionalEmbeddings(4)` succeeds on the same tensor shape.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
