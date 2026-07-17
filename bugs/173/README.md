# Bug 173 Reproduction

This folder reproduces the dependency conflict reported in Kubeflow Katib issue `#2346`.

## What fails

Installing these two package versions together fails:

- `kfp==2.7.0`
- `kubeflow-katib==0.17.0rc0`

The resolver conflict is on `kubernetes`:

- `kfp==2.7.0` requires `kubernetes<27,>=8.0.0`
- `kubeflow-katib==0.17.0rc0` requires `kubernetes>=27.2.0`

## Repro

Run:

```bash
bash run_repro.sh
```

The script writes:

- `repro_stdout.log`
- `repro_stderr.log`
- `reproduction.json`

## Files

- `repro.py`: resolver repro
- `requirements.txt`: helper runtime dependency pin
- `setup_env.sh`: creates a virtual environment and upgrades packaging tools
- `run_repro.sh`: executes the repro
- `manifest.json`: standardized metadata for the bug folder

