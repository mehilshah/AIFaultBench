# Accelerate bug repro

This folder reproduces the `accelerate test` failure from
[`huggingface/accelerate#898`](https://github.com/huggingface/accelerate/issues/898).

Observed failure:

```text
AttributeError: 'Namespace' object has no attribute 'use_cpu'
```

Repro flow:

1. Run `bash setup_env.sh`
2. Run `bash run_repro.sh`
3. Inspect `repro_stdout.log`, `repro_stderr.log`, and `reproduction.json`

Files in this bundle:

- `repro.py`: launches `accelerate test` with the SageMaker config from the issue
- `sagemaker_default_config.yaml`: config file that triggers the bug on `accelerate==0.14.0`
- `requirements.txt`: minimal dependency set for the repro
- `setup_env.sh`: creates a Python 3.10 virtualenv and installs the pinned deps
- `run_repro.sh`: runs the repro and captures logs
- `manifest.json`: metadata for the bundle
