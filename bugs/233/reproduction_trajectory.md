# Reproduction Trajectory — Bug 233: equinox

- **Bug report:** [https://github.com/patrick-kidger/equinox/issues/1089](https://github.com/patrick-kidger/equinox/issues/1089)
- **Repository:** patrick-kidger/equinox @ `6a6a441`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a local venv with `bash setup_env.sh`.
2. Run `bash run_repro.sh`.
3. Inspect `repro_stdout.log` and `repro_stderr.log` for the `Non-hashable static arguments are not supported` traceback.

## Observed behavior

- On Python 3.11.15 with Equinox 0.13.0 and JAX 0.4.38, `jax.jit(..., static_argnames='static')` raised `ValueError: Non-hashable static arguments are not supported` because `Problematic.__hash__` tried to hash a `dict` field and failed with `TypeError: unhashable type: 'dict'`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
