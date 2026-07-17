# Reproduction Trajectory — Bug 277: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2181](https://github.com/pyro-ppl/numpyro/issues/2181)
- **Repository:** pyro-ppl/numpyro @ `e708f34b1c0b2c37137196281ba1486be7bebf39`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtual environment and installed numpy, scipy, jax[cpu], multipledispatch, and tqdm.
2. Imported the local NumPyro codebase from codebase/.
3. Evaluated Poisson(2).log_prob(1.999999) and Poisson(2.0).log_prob(1.999999).
4. Observed a 0.6931464672088623 absolute difference between the two log probabilities.

## Observed behavior

- Running the local repro against codebase/ produced different results for the same value: Poisson(2).log_prob(1.999999) = -2.000000238418579, while Poisson(2.0).log_prob(1.999999) = -1.3068537712097168.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
