# Reproduction Trajectory — Bug 038: labml-nn

- **Bug report:** [https://github.com/labmlai/annotated_deep_learning_paper_implementations/issues/244](https://github.com/labmlai/annotated_deep_learning_paper_implementations/issues/244)
- **Repository:** labmlai/annotated_deep_learning_paper_implementations @ `a0679ecd90b41b8e012995a6bdf095edae590b17`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtual environment and installed the minimal dependencies from requirements.txt.
2. Loaded the RoPE implementation directly from codebase/labml_nn/transformers/rope/__init__.py with import stubs for unrelated modules.
3. Called RotaryPositionalEmbeddings(3) on a tensor shaped (3, 1, 1, 4).
4. Observed the tensor size mismatch at the RoPE multiplication line.

## Observed behavior

- bash run_repro.sh reproduces a RuntimeError in codebase/labml_nn/transformers/rope/__init__.py:188.
- The failing input is input_shape=(3, 1, 1, 4) with rope_features=3.
- Observed message: The size of tensor a (3) must match the size of tensor b (4) at non-singleton dimension 3.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
