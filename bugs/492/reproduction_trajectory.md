# Reproduction Trajectory — Bug 492: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2040](https://github.com/pyro-ppl/numpyro/issues/2040)
- **Repository:** pyro-ppl/numpyro @ `7a3c24ff4b072f3f3df6c0ef9494d1635753c53d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create an isolated Python virtual environment.
2. Install the pinned requirements from requirements.txt.
3. Run repro.py via run_repro.sh and observe the import-time traceback.

## Observed behavior

- In a fresh venv, installing numpyro==0.10.1 with jax==0.4.38 and jaxlib==0.4.38 then running import numpyro fails during import. The captured stderr ends with ModuleNotFoundError: No module named 'jax.linear_util' from numpyro/ops/provenance.py.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
