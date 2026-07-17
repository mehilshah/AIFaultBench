# Bug 045 Reproduction Bundle

This folder contains a minimal reproduction for fairseq issue #5320.

The failure is a structured-config write error in `speech_to_speech`:

- `codebase/fairseq/tasks/speech_to_speech.py:337`
- `codebase/fairseq/data/audio/data_cfg.py:96`

The reported behavior is a `ConfigAttributeError` / `ConfigKeyError` saying:

`Key 'input_feat_per_channel' is not in struct`

## What reproduces

`repro.py` constructs the same kind of structured OmegaConf object that fairseq's generation path uses and then performs the assignment that fails in the bug report.

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```

## Files

- `repro.py`: minimal failing reproduction
- `requirements.txt`: runtime dependency pin for the repro
- `setup_env.sh`: creates a local virtualenv and installs the requirements
- `run_repro.sh`: executes the repro
- `manifest.json`: standardized metadata for the bug folder
- `reproduction.json`: machine-readable outcome
- `repro_stdout.log`, `repro_stderr.log`: captured run output
