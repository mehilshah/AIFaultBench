# Reproduction Trajectory — Bug 331: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/47228](https://github.com/huggingface/transformers/issues/47228)
- **Repository:** huggingface/transformers @ `0bc355418bb265136a66c2dedc501066ffbc237d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run `bash setup_env.sh` to create `.venv` and install dependencies.
2. Run `bash run_repro.sh` from the bug folder.
3. Observe that eager inference succeeds and the compiled forward fails in `repro.py`.

## Observed behavior

- A tiny bf16 Sam3Model run succeeded eagerly and failed under torch.compile with `RuntimeError: mat1 and mat2 must have the same dtype, but got Float and BFloat16`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
