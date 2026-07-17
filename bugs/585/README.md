# Bug 585 Reproduction

This folder reproduces the `accelerate launch` exit-code bug reported in
https://github.com/huggingface/accelerate/issues/996.

The key failure path is the distributed launcher in
[`codebase/src/accelerate/commands/launch.py`](codebase/src/accelerate/commands/launch.py):
an exception raised by `torch.distributed.run.run(...)` is swallowed, so the CLI
returns exit code `0` even though the launch failed.

## Files

- `repro.py`: runs the reproducible check.
- `sitecustomize.py`: injects a failing `torch.distributed.run.run`.
- `requirements.txt`: minimal runtime dependencies.
- `setup_env.sh`: creates a clean virtual environment and installs deps.
- `run_repro.sh`: runs the repro and captures logs.
- `reproduction.json`: machine-readable reproduction result.

## Run

```bash
./setup_env.sh
./run_repro.sh
cat reproduction.json
```

The repro is considered successful when `accelerate launch --multi_gpu` exits
with code `0` after the injected failure.
