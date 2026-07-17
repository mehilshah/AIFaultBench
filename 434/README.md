# Bug 434

This folder contains a self-contained reproduction bundle for the Gemma4 dtype-casting bug described in `bug_report.txt`.

What the repro checks:
- the local transformers checkout still contains the unsafe casts in `codebase/src/transformers/models/gemma4/modeling_gemma4.py`
- a float activation tensor becomes integer-truncated when cast to the dtype of a quantized weight tensor
- the fixed behavior would skip the cast when the target dtype is not floating-point

Files:
- `bug_report.txt`
- `codebase/`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Run locally:
```bash
bash setup_env.sh
bash run_repro.sh
```

The repro exits non-zero when the bug is reproduced. The captured output in `repro_stdout.log` and `repro_stderr.log` shows the source lines and the truncation behavior.
