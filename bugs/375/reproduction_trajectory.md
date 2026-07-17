# Reproduction Trajectory — Bug 375: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/38634](https://github.com/jax-ml/jax/issues/38634)
- **Repository:** jax-ml/jax @ `faf677af0abec7ea25c7a33831fcabf30a795796`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create and activate a local virtual environment.
2. Install the pinned repro dependencies from requirements.txt.
3. Run repro.py through run_repro.sh on the CPU backend.

## Observed behavior

- Running the repro under jax==0.10.1 and jaxlib==0.10.1 on CPU prints actual=[[inf, inf, inf], [inf, 4.76837158203125e-07, 13.815508842468262]] while the expected value for the smallest positive float32 subnormal is 103.2789306640625; the script raises AssertionError because the subnormal input is returned as inf.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
