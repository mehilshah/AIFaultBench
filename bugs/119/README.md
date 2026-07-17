# Bug 119

This folder contains a standalone reproduction bundle for the GPyTorch TorchScript fantasy-model bug.

Reproduction command:

```bash
bash run_repro.sh
```

Observed failure:

`RuntimeError: Cannot insert a Tensor that requires grad as a constant.`

Artifacts:

- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Inputs preserved from the standardized source:

- `bug_report.txt`
- `codebase/`
