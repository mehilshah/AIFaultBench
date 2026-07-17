# Reproduction Trajectory — Bug 224: adversarial-robustness-toolbox

- **Bug report:** [https://github.com/Trusted-AI/adversarial-robustness-toolbox/issues/2473](https://github.com/Trusted-AI/adversarial-robustness-toolbox/issues/2473)
- **Repository:** Trusted-AI/adversarial-robustness-toolbox @ `a5a61d3`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run bash run_repro.sh from the standardized bug folder.
2. The script simulates the reported torchvision version string 0.18.1a0+405940f.
3. The ART parsing logic from art/estimators/object_detection/pytorch_object_detector.py:L98 raises ValueError when it attempts int('1a0').

## Observed behavior

- Running bash run_repro.sh prints torchvision.__version__=0.18.1a0+405940f and then fails in the exact ART parsing expression with ValueError: invalid literal for int() with base 10: '1a0'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
