# Bug 071

This folder reproduces the DeepSpeed-Chat import failure reported in
`bug_report.txt`.

## Root Cause

`codebase/applications/DeepSpeed-Chat/dschat/utils/model/model_utils.py` imports:

```python
from transformers.deepspeed import HfDeepSpeedConfig
```

On current `transformers` releases, that submodule is absent, so the import
raises:

```text
ModuleNotFoundError: No module named 'transformers.deepspeed'
```

## Reproduction

```bash
bash run_repro.sh
```

The script:

1. Creates a local virtual environment.
2. Installs `transformers==5.14.1`.
3. Runs `repro.py`, which imports the missing module path and records output in:
   - `repro_stdout.log`
   - `repro_stderr.log`

## Expected Result

The reproduction is successful when the process exits non-zero and the stderr log
contains `ModuleNotFoundError: No module named 'transformers.deepspeed'`.
