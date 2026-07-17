# Reproduction Trajectory — Bug 566: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2714](https://github.com/sdv-dev/SDV/issues/2714)
- **Repository:** sdv-dev/SDV @ `ae6e1c01a9b4d06bbc13868071a3ec36c5ed2d33`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a Python 3.11 venv and installed the SDV runtime dependencies.
2. Ran the issue's reported PARSynthesizer configuration against synthetic data shaped like the bug report.
3. Ran a control configuration with aligned column ordering to confirm the model still fits and samples.

## Observed behavior

- The reported sample-time KeyError ('KeyError: 58.0') was not reproduced. With the issue report's column order, fit() fails earlier with a TypeError from deepecho's context type inference. With an aligned control ordering, fit() and sample() both succeed.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The exact reported KeyError is not reachable from the reproduced inputs here; the reported context ordering fails earlier in fit(), and the aligned control case does not error.
