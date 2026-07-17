# Bug 501

This folder is the reusable standardized benchmark input for this bug.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/` when available

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction summary:
- A clean CPU install of DeepSpeed `0.18.5` from `codebase/` was exercised with a one-stage `PipelineModule`.
- The same 8-sample global batch was run twice: once with `gradient_accumulation_steps=1` and once with `gradient_accumulation_steps=4`.
- The custom optimizer recorded identical pre-step gradient norms in both runs, so the reported bug did not reproduce here.

Source summary:
- issue URL: `https://github.com/deepspeedai/DeepSpeed/issues/7773`
- commit hash: `8a9369d03e800e413a31503ceb0e5d39e390d845`
- inferred library: `DeepSpeed`
- inferred library version: `0.18.5`
- bug report source: `bug_report.txt`
- codebase source: `microsoft/DeepSpeed@8a9369d03e800e413a31503ceb0e5d39e390d845`
