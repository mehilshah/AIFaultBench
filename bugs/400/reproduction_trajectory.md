# Reproduction Trajectory — Bug 400: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2093](https://github.com/pyro-ppl/numpyro/issues/2093)
- **Repository:** pyro-ppl/numpyro @ `d49f71825691b554fb8188f8779dc3a5d13e7b96`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create and activate the local virtual environment with `bash setup_env.sh`.
2. Run the repro with `bash run_repro.sh`.
3. Observe that the out-of-support density is non-zero instead of zero.

## Observed behavior

- Running `bash run_repro.sh` after `bash setup_env.sh` prints `log_prob=-1.6094379425048828` and `density=0.19999998807907104` for `Uniform(0.0, 5.0).log_prob(7.0)`, then fails with `AssertionError: Expected zero density outside the support`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
