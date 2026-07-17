# Reproduction Trajectory — Bug 039: annotated_deep_learning_paper_implementations

- **Bug report:** [https://github.com/labmlai/annotated_deep_learning_paper_implementations/issues/215](https://github.com/labmlai/annotated_deep_learning_paper_implementations/issues/215)
- **Repository:** labmlai/annotated_deep_learning_paper_implementations @ `732aedcfc664d032f3a9b90c623e1dbe9ef3fba9`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create the virtual environment and install dependencies with bash setup_env.sh.
2. Run bash run_repro.sh from the bug folder.
3. Observe the RoPE forward pass fail with a dimension-3 mismatch in codebase/labml_nn/transformers/rope/__init__.py.

## Observed behavior

- Running repro.py with torch inputs shaped (3, 1, 1, 4) and RotaryPositionalEmbeddings(3) raises RuntimeError: The size of tensor a (3) must match the size of tensor b (4) at non-singleton dimension 3.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
