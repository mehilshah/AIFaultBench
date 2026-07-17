# Bug 241

This folder is the reusable standardized benchmark input for the NumPyro issue
reported at `https://github.com/pyro-ppl/numpyro/issues/1916`.

What reproduces here:
- `MCMC.warmup(...)` with `AIES` succeeds.
- A later `MCMC.run(...)` reuses the warmup state and fails with:
  `ValueError: split accepts a single key, but was given a key array of shape (100, 2) != (). Use jax.vmap for batching.`

Bundle contents:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Environment used for verification:
- `numpyro==0.15.3`
- `jax==0.4.25`
- `jaxlib==0.4.25`
- `numpy<2`

Run:
```bash
bash run_repro.sh
```
