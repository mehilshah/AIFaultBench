# Bug 352

This folder contains a self-contained reproduction bundle for PEFT issue `#1938`.

Bug summary:
- Prefix tuning in `PeftModelForCausalLM.forward()` forwards a generated `past_key_values` argument with `**kwargs`.
- If the caller also supplies `past_key_values`, Python raises `TypeError: got multiple values for keyword argument 'past_key_values'`.

Local inputs used:
- `bug_report.txt`
- `codebase/`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

How to run:
```bash
bash run_repro.sh
cat reproduction.json
```

Observed outcome in this snapshot:
- `reproducible`: `false`
- The tiny prefix-tuning forward pass completed without the duplicate-keyword `TypeError`.
- See `reproduction.json` for the exact evidence string and blocking reason.
