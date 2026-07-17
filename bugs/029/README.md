# Reproduction Bundle

This folder contains a self-contained repro for the ImageNet example crash
reported in pytorch/examples issue 1134.

What is included:
- `bug_report.txt` and `codebase/` from the standardized input
- `repro.py` to trigger the failure
- `requirements.txt` with the runtime dependencies
- `setup_env.sh` to create an isolated environment
- `run_repro.sh` to execute the repro
- `manifest.json` with source metadata
- `reproduction.json` with the reproduction result
- `repro_stdout.log` and `repro_stderr.log` with command output

The repro intentionally removes `torch.backends.mps` at runtime before running
`codebase/imagenet/main.py --dummy`, matching the compatibility failure in the
bug report when code accesses `torch.backends.mps.is_available()` on a build
where that backend is absent.
