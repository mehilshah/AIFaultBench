# Bug 421

This folder contains a self-contained reproduction bundle for diffusers issue 13967.

## What fails

`ErnieImageModularPipeline` inherits only from `ModularPipeline`, while the non-modular ERNIE image pipeline mixes in `ErnieImageLoraLoaderMixin`. As a result, the modular pipeline instance does not expose `load_lora_weights()`.

## Files

- `bug_report.txt`: recovered issue text
- `codebase/`: pinned diffusers source snapshot
- `repro.py`: deterministic repro script
- `requirements.txt`: minimal Python dependencies for the repro harness
- `setup_env.sh`: install dependencies
- `run_repro.sh`: execute the repro and capture logs
- `manifest.json`: bundle metadata
- `reproduction.json`: schema-constrained repro result
- `repro_stdout.log` / `repro_stderr.log`: command output

## Run

```bash
bash setup_env.sh
bash run_repro.sh
cat reproduction.json
```
