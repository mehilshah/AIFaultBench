# Bug 121 Reproduction Bundle

This folder contains a self-contained repro for Stable-Baselines3 issue 1900.

What it does:
- creates a `PPO` model with `learning_rate=lambda _: np.sin(1.0)`
- saves the model
- loads it again with `PPO.load(...)`
- reproduces the `torch.load(..., weights_only=True)` failure on the saved zip archive

Key files:
- `bug_report.txt`: original report
- `codebase/`: local SB3 source snapshot used for the repro
- `repro.py`: minimal Python reproduction
- `requirements.txt`: runtime dependencies for the repro
- `setup_env.sh`: creates a local virtualenv and installs dependencies
- `run_repro.sh`: runs the repro and writes `repro_stdout.log` / `repro_stderr.log`
- `reproduction.json`: schema-constrained repro result

Run it locally:
```bash
bash setup_env.sh
bash run_repro.sh
```

The repro is expected to fail at load time with:
- `UnpicklingError`
- `Weights only load failed`
- `Unsupported global: GLOBAL numpy.core.multiarray.scalar`
