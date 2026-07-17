# SDV issue 1741 reproduction

This bundle reproduces the bug described in `bug_report.txt`:

`CTGANSynthesizer`, `TVAESynthesizer`, and `CopulaGANSynthesizer` reach a state where
`fit()` completes without training a model, and `sample()` then raises:

`AttributeError: '...Synthesizer' object has no attribute '_model'`

## Files

- `repro.py`: Minimal reproduction script.
- `requirements.txt`: Runtime dependencies for the repro environment.
- `setup_env.sh`: Creates a venv and installs dependencies plus the local package.
- `run_repro.sh`: Runs the repro and writes `repro_stdout.log` and `repro_stderr.log`.
- `reproduction.json`: Final machine-readable result.

## Run

```bash
bash run_repro.sh
```
