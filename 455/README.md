# Bug 455

This folder is the reusable standardized benchmark input for this bug.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/` from `huggingface/peft@cc82b674b5db38b9a393463d38afe66e8f48ac1c`

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction command:
`bash setup_env.sh && bash run_repro.sh`

Source summary:
- issue URL: `https://github.com/huggingface/peft/issues/297`
- commit hash: `cc82b674b5db38b9a393463d38afe66e8f48ac1c`
- inferred library: `peft`
- inferred library version: `0.3.0.dev0`
- bug report source: `bug_report.txt`
- codebase source: `huggingface/peft@cc82b674b5db38b9a393463d38afe66e8f48ac1c`
