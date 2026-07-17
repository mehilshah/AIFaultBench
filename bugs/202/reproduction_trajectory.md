# Reproduction Trajectory — Bug 202: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/1719](https://github.com/pyro-ppl/numpyro/issues/1719)
- **Repository:** pyro-ppl/numpyro @ `d28fd82`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtual environment and installed the pinned runtime dependencies from `requirements.txt` against the local `codebase/` tree.
2. Ran `bash run_repro.sh`, which executes the report's NUTS model with `jump=1000.0`, `num_warmup=2000`, and `num_samples=20000`.
3. Observed a posterior mean of `0.739689`, which is materially below the half-normal mean `0.797885`.

## Observed behavior

- On the checked-out codebase, `bash run_repro.sh` produced `sample_mean=0.739689` versus the half-normal mean `0.797885`, with `mean_error=-0.058196` and `num_diverging=8522`. The posterior is biased low relative to the expected positive half-normal target.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
