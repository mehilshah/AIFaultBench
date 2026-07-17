# Reproduction Trajectory — Bug 371: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2123](https://github.com/pyro-ppl/numpyro/issues/2123)
- **Repository:** pyro-ppl/numpyro @ `4fd6c733a82c30b7449c5fff3015f2bcb5cc30b7`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a Python 3.12 virtualenv and installed jax 0.8.2, jaxlib 0.8.2, graphviz, multipledispatch, and tqdm.
2. Installed the local codebase in editable mode from ./codebase.
3. Ran the reported model-rendering repro and observed the batched Uniform mixture print (2,) twice, while the list-of-Uniform mixture printed () twice.

## Observed behavior

- Running ./run_repro.sh prints '(2,)\n(2,)\n()\n()'. The batched Uniform mixture produces theta.shape == (2,) twice, while the list-of-Uniform mixture produces theta.shape == () twice.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
