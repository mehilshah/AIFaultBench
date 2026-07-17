# Reproduction Trajectory — Bug 111: pygad

- **Bug report:** [https://github.com/ahmedfgad/GeneticAlgorithmPython/issues/335](https://github.com/ahmedfgad/GeneticAlgorithmPython/issues/335)
- **Repository:** ahmedfgad/GeneticAlgorithmPython @ `9ac7527`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a virtualenv and installed the bug-specific dependencies from requirements.txt.
2. Ran repro.py against the local codebase snapshot with init_range_low=0, init_range_high=2, gene_type=int, and random_seed=0.
3. Observed best_solution values below the configured lower bound: solution_min=-14.

## Observed behavior

- With random_seed=0, the best solution contained negative genes even though init_range_low=0. The repro printed solution_min=-14 and the marker BUG_REPRODUCED.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh > repro_stdout.log 2> repro_stderr.log
```
