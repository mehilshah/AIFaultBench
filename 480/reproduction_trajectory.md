# Reproduction Trajectory — Bug 480: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2051](https://github.com/pyro-ppl/numpyro/issues/2051)
- **Repository:** pyro-ppl/numpyro @ `0d4f40c5a25633591388f12372cdb31f9dff0f29`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a fresh Python virtual environment with `setup_env.sh`.
2. Install `jax==0.7.0`, `jaxlib==0.7.0`, and `numpyro==0.18.0`.
3. Run `run_repro.sh` to execute `repro.py`.
4. Observe the import failure in `repro_stderr.log`.

## Observed behavior

- Running `import numpyro` with `numpyro==0.18.0`, `jax==0.7.0`, and `jaxlib==0.7.0` fails during import with `ImportError: cannot import name 'pjit_p' from 'jax.experimental.pjit'`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
