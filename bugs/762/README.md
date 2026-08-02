# Bug 762

The non-streaming Temporal model-request activity patches its `deps` annotation after Temporal has captured its argument types. This offline repro compares Temporal's captured types for the non-streaming and streaming activities, and exits with status 1 when the non-streaming activity has retained `typing.Any | None` instead of the declared dataclass type.

On this host the bug reproduces with the pinned checkout and `temporalio==1.27.2`.

Files: `repro.py` is the failing check; `requirements.txt`, `setup_env.sh`, and `run_repro.sh` build and run it; `repro_stdout.log` and `repro_stderr.log` contain final-run evidence; `reproduction.json` and `reproduction_trajectory.md` record the result.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
