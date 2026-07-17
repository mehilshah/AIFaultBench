# Reproduction Trajectory — Bug 590: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2013](https://github.com/pyro-ppl/numpyro/issues/2013)
- **Repository:** pyro-ppl/numpyro @ `ab1f0dc6e954ef7d54724386667e33010b2cfc8b`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated venv with `bash setup_env.sh` using the pinned dependency set in `requirements.txt`.
2. Ran `bash run_repro.sh` with `PYTHONPATH` pointing at the local `codebase/` checkout.
3. Observed `TraceEnum_ELBO` crash with `KeyError: 'aux'` when the guide included `infer={'is_auxiliary': True}` for a site absent from the model.

## Observed behavior

- With jax==0.4.25, jaxlib==0.4.25, numpy==1.26.4, scipy==1.11.4, and funsor==0.4.7, `bash run_repro.sh` runs `TraceEnum_ELBO().loss(...)` and fails with `KeyError: 'aux'` in `codebase/numpyro/infer/elbo.py:982` while iterating over guide sample sites. The captured stderr is stored in `repro_stderr.log`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
