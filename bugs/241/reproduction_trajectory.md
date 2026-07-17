# Reproduction Trajectory — Bug 241: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/1916](https://github.com/pyro-ppl/numpyro/issues/1916)
- **Repository:** pyro-ppl/numpyro @ `f87f40e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create an AIES kernel around the bug report's 5D Normal model with 100 vectorized chains.
2. Run `MCMC.warmup` with `jax.random.PRNGKey(0)` and confirm it completes.
3. Call `MCMC.run` with a fresh key and observe the PRNG split ValueError from `numpyro/infer/ensemble.py`.

## Observed behavior

- Using numpyro 0.15.3 with jax 0.4.25 and numpy<2, `mcmc.warmup(...)` completes, printing `warmup_ok=True`, and the subsequent `mcmc.run(...)` raises `ValueError: split accepts a single key, but was given a key array of shape (100, 2) != (). Use jax.vmap for batching.` The repro logs also show `run_failed=ValueError` immediately before the traceback.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
