# Reproduction Trajectory — Bug 203: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/1911](https://github.com/pyro-ppl/numpyro/issues/1911)
- **Repository:** pyro-ppl/numpyro @ `66921bd`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a virtual environment and install the repro dependencies from `requirements.txt`.
2. Run `bash run_repro.sh` from the standardized bug folder.
3. Observe that `mcmc.get_samples()` prints `{}` and the summary call crashes with the reported `ValueError`.

## Observed behavior

- Running the local NumPyro checkout with a model containing only `numpyro.deterministic` sites produces `samples = {}` and `mcmc.print_summary()` raises `ValueError: max() iterable argument is empty` in `numpyro/diagnostics.py:311`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
