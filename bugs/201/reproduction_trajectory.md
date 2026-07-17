# Reproduction Trajectory — Bug 201: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/1713](https://github.com/pyro-ppl/numpyro/issues/1713)
- **Repository:** pyro-ppl/numpyro @ `9ce2384`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create and activate the local virtual environment with `bash setup_env.sh`.
2. Run the repro with `bash run_repro.sh`.
3. Observe that `AutoNormal` finishes and `AutoDiagonalNormal` fails with the reported `KeyError`.

## Observed behavior

- With numpyro 0.13.2, jax 0.4.23, jaxlib 0.4.23, numpy 1.26.4, scipy 1.12.0, and funsor 0.4.7, `AutoNormal` completes but `AutoDiagonalNormal` under `TraceEnum_ELBO` raises `KeyError: 'components'` from `numpyro/contrib/funsor/enum_messenger.py:429` when entering the `components` plate.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
