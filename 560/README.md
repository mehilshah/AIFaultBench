# Bug 560 Reproduction

This folder reproduces DeepSpeed issue 7729 locally from the provided `bug_report.txt` and `codebase/`.

## What it does

- Creates a CPU-only virtualenv in `.venv_repro`
- Installs the minimum runtime dependencies from `requirements.txt`
- Runs `repro.py` under `torch.distributed.run` with 2 local ranks
- Passes a PEFT-wrapped `LlamaForCausalLM` instance into `UlyssesSPAttentionHF.register_with_transformers()`

## Expected result

The bug triggers when DeepSpeed falls through to `AutoConfig.from_pretrained(...)` with a `PeftModel` object, which is not a valid path or model identifier.

## Files

- `repro.py`: minimal distributed reproduction
- `requirements.txt`: Python dependencies for the repro env
- `setup_env.sh`: creates and populates `.venv_repro`
- `run_repro.sh`: launches the repro and captures logs
- `repro_stdout.log` / `repro_stderr.log`: captured command output
- `reproduction.json`: schema-constrained result
