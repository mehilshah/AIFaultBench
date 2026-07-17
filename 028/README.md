# Bug 028 Reproduction

This bundle reproduces the `vision_transformer` CIFAR-10 default mismatch in `codebase/vision_transformer/main.py`.

Observed issue:
- `--num-classes` defaults to `16`
- the inline help text says the CIFAR-10 default should be `10`

Files:
- `repro.py`: static offline repro that extracts the `--num-classes` default from the source
- `run_repro.sh`: runs the repro and writes `repro_stdout.log` / `repro_stderr.log`
- `requirements.txt`: empty because the repro only uses the Python standard library
- `setup_env.sh`: minimal environment check

Run locally:
```bash
bash setup_env.sh
bash run_repro.sh
```

Expected result:
- the script exits non-zero and reports that the source uses `16` instead of the CIFAR-10 default `10`
