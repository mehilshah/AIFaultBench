# Reproduction Trajectory — Bug 036: annotated_deep_learning_paper_implementations

- **Bug report:** [https://github.com/labmlai/annotated_deep_learning_paper_implementations/issues/255](https://github.com/labmlai/annotated_deep_learning_paper_implementations/issues/255)
- **Repository:** labmlai/annotated_deep_learning_paper_implementations @ `999f2036a5a7c54403352211b5d1cc0df42b83f6`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. bash setup_env.sh
2. bash run_repro.sh

## Observed behavior

- repro_stdout.log shows codebase/labml_nn/rl/ppo/gae.py lines 36 and 45 still contain the reported formula mistakes.
- repro_stderr.log shows AssertionError: GAE docstring is still incorrect because the infinite-horizon term uses r_{t+1} instead of r_{t+2}, and the weights omit the (1-lambda) factor.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
