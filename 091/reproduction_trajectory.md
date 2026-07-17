# Reproduction Trajectory — Bug 091: x-transformers

- **Bug report:** [https://github.com/lucidrains/x-transformers/issues/271](https://github.com/lucidrains/x-transformers/issues/271)
- **Repository:** lucidrains/x-transformers @ `6db4d225fb3fb95cbdb480bdec0a71313f2666f0`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create the local virtual environment and install the pinned CPU dependencies from requirements.txt.
2. Run repro.py through run_repro.sh using the local codebase snapshot.
3. Observe that training/backward complete, then generate() crashes with the 258-vs-30 mask shape mismatch.

## Observed behavior

- Running the local repro on CPU reaches model.generate and then fails with RuntimeError: The size of tensor a (258) must match the size of tensor b (30) at non-singleton dimension 3. The traceback points to x_transformers/attend.py masked_fill during decoder cross-attention.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
