# Reproduction Trajectory — Bug 238: jaxtyping

- **Bug report:** [https://github.com/patrick-kidger/jaxtyping/issues/349](https://github.com/patrick-kidger/jaxtyping/issues/349)
- **Repository:** patrick-kidger/jaxtyping @ `fe61644`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated .venv with Python 3.12.
2. Installed editable local codebase plus jax[cpu]>=0.4.31, numpy<2, and typeguard==2.13.3.
3. Ran ./run_repro.sh against repro.py.

## Observed behavior

- with_optional rejected the float array
- with_union rejected the float array
- with_pipe accepted the float array, matching the reported bug

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
