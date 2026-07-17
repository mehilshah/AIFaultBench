# Reproduction Trajectory — Bug 363: whisperx

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21693](https://github.com/Lightning-AI/pytorch-lightning/issues/21693)
- **Repository:** Lightning-AI/pytorch-lightning @ `0e20e15f2376f4f356470b08875639a945c43334`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a clean Python 3.12 virtual environment with `setup_env.sh`.
2. Executed `repro.py`, which runs `pip install --dry-run --isolated whisperx==3.4.3`.
3. Observed a successful dependency resolution instead of the expected `lightning>=2.0.1` installation failure.

## Observed behavior

- Running `python3 -m pip install --dry-run --isolated whisperx==3.4.3` inside a fresh virtual environment exited with code 0.
- The resolver output ended with `Would install ... lightning-2.6.5 ... pyannote.audio-3.4.0 ... whisperx-3.4.3`, which means the current package index no longer reproduces the quarantined-lightning conflict from the report.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The current PyPI state differs from the report: `lightning` is installable again, so `whisperx==3.4.3` resolves successfully and the original uninstallable-dependency bug is no longer present in this environment.
