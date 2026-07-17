# Reproduction Trajectory — Bug 356: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2130](https://github.com/pyro-ppl/numpyro/issues/2130)
- **Repository:** pyro-ppl/numpyro @ `c5fce4e3df4699e3913e0538fe3efffcabbc026b`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a local virtual environment and installed the bug-specific runtime dependencies from requirements.txt.
2. Loaded codebase/numpyro/distributions/__init__.py in isolation without executing numpyro.__init__.
3. Verified that numpyro.distributions.InverseWishart exists in this checkout.
4. Attempted the standard import path and observed it fail earlier on the unrelated JAX compatibility issue.

## Observed behavior

- codebase/numpyro/distributions/__init__.py imports InverseWishart directly into the public namespace.
- repro_stdout.log shows an isolated load of numpyro.distributions with InverseWishart_present=True.
- repro_stderr.log shows the full import path is blocked earlier by an unrelated JAX API mismatch: ImportError: cannot import name 'debug_info' from 'jax.api_util'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported AttributeError is not reproducible in this checkout because the source tree already exports InverseWishart. The only failing import path here is an unrelated JAX API mismatch in numpyro.__init__/numpyro.ops.provenance.
