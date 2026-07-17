# Reproduction Trajectory — Bug 415: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2088](https://github.com/pyro-ppl/numpyro/issues/2088)
- **Repository:** pyro-ppl/numpyro @ `ee8dbcb9a53dd42abc7a8ae2ffb9585a24ff3490`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a clean virtual environment.
2. Installed the pinned dependencies from requirements.txt.
3. Ran repro.py through run_repro.sh.
4. Observed nan from Beta(1.0, 8.0).log_prob(0.0).

## Observed behavior

- A clean virtual environment with numpyro==0.19.0, jax==0.4.38, and jaxlib==0.4.38 printed nan for Beta(1.0, 8.0).log_prob(0.0) and jnp.isnan(...) was True.
- The same expression is the boundary-value case described in bug_report.txt and is the one asserted in repro.py.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
