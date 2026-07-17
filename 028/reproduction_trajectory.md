# Reproduction Trajectory — Bug 028: examples

- **Bug report:** [https://github.com/pytorch/examples/issues/1175](https://github.com/pytorch/examples/issues/1175)
- **Repository:** pytorch/examples @ `6fc19c76b9f5550d8d3cb38284845ac7ed14223c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Inspect codebase/vision_transformer/main.py
2. Extract the --num-classes argparse default value
3. Compare the observed default against the CIFAR-10 expectation of 10

## Observed behavior

- python3 repro.py prints num_classes_default=16 from codebase/vision_transformer/main.py
- stderr reports: BUG: expected default num_classes=10 for CIFAR10, but code sets 16.
- run_repro.sh exits with code 1

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
