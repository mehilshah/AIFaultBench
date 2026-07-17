# Reproduction Trajectory — Bug 231: optuna

- **Bug report:** [https://github.com/optuna/optuna/issues/6073](https://github.com/optuna/optuna/issues/6073)
- **Repository:** optuna/optuna @ `632ab66`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a GridSampler study over the 2x2 categorical search space from the bug report.
2. Enqueue the first grid point with `study.enqueue_trial({"c0": "0", "c1": "0"})`.
3. Run `study.optimize(...)` and inspect the resulting trials.
4. Observe that the enqueued point is evaluated twice instead of being consumed once.

## Observed behavior

- Running `bash run_repro.sh` produced 5 trials total. The enqueued parameters {"c0": "0", "c1": "0"} appeared twice: once as trial 0 and again as trial 3. The repro script reported `target_occurrences=2` and `BUG REPRODUCED`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
