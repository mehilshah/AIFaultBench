# Bug 182

This folder reproduces a Lightning bug where `LightningModule.save_hyperparameters()` crashes on a dataclass field declared with `init=False`.

Observed failure:

```text
AttributeError: 'Module' object has no attribute 'not_a_param'
```

Key files:
- `bug_report.txt`
- `codebase/`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction:

1. Run `bash setup_env.sh`
1. Run `bash run_repro.sh`

The repro uses the local source tree via `codebase/src` and a CPU-only Torch wheel to avoid the broken host Torch install.
