# Bug 599

This folder reproduces DeepSpeed issue 7711.

Bug summary:
- `OpenMPIRunner` validates `OMPI_COMM_WORLD_*` environment variables during construction.
- That validation runs before `mpirun` can set the variables, so a normal `--launcher=OPENMPI` launch fails with `OSError: MPI environment variables are not set.`

Repro artifacts in this folder:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

How to run:
- `bash run_repro.sh`

Source inputs:
- issue URL: `https://github.com/deepspeedai/DeepSpeed/issues/7711`
- bug report: `bug_report.txt`
- codebase: `codebase/`
