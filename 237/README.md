# Bug 237 Reproduction Bundle

This folder contains a minimal repro for the verbose `TypeCheckError` formatting issue in `jaxtyping`.

## What it does

The repro calls a `jaxtyped` `torch.matmul` wrapper with mismatched matrix shapes. The resulting `TypeCheckError` still embeds the full tensor repr for the bad argument instead of a compact summary.

## Files

- `repro.py` - self-checking reproducer
- `requirements.txt` - runtime dependencies
- `setup_env.sh` - creates `.venv` and installs dependencies
- `run_repro.sh` - runs the repro and writes `repro_stdout.log` / `repro_stderr.log`
- `manifest.json` - standardized metadata

## Run

```bash
bash setup_env.sh
bash run_repro.sh
cat repro_stdout.log
cat repro_stderr.log
```
