# Reproduction Trajectory — Bug 602: rl

- **Bug report:** [https://github.com/pytorch/rl/issues/3244](https://github.com/pytorch/rl/issues/3244)
- **Repository:** pytorch/rl @ `8570c25a745da54ca647b8a70231112f063d1421`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created an isolated virtual environment and installed the minimal TorchRL dependencies.
2. Added the local `codebase/` directory to `PYTHONPATH` and ran the exact constructor from the report.
3. Verified that the VIP model downloaded and loaded successfully instead of failing.

## Observed behavior

- In a clean Python 3.12 venv with torch 2.5.1+cpu, torchvision 0.20.1+cpu, and tensordict 0.10.0, `VIPTransform(model_name='resnet50', download=True)` completed successfully. The VIP weights URL `https://pytorch.s3.amazonaws.com/models/rl/vip/model.pt` returned HTTP 200 and the constructor finished without raising.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported failure is not reproducible in this environment because the VIP weights URL is reachable and the constructor succeeds.
