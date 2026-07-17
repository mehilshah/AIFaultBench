# Bug 584

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

Reproduction target:
- `DistributedSamplerWrapper.set_epoch()` in `codebase/src/lightning/fabric/utilities/distributed.py`

Expected behavior:
- The wrapped sampler should receive the same `set_epoch()` call that the wrapper receives.

Observed behavior:
- The wrapped sampler's `set_epoch()` is never called.

Run the repro:
`bash setup_env.sh && bash run_repro.sh`

Source summary:
- issue URL: `https://github.com/Lightning-AI/pytorch-lightning/issues/21454`
- commit hash: `027455bcd9433f201b1136f68d54b1a07588abe3`
- inferred library: `pytorch-lightning`
- inferred library version: `2.6.0`
- bug report source: `bug_report.txt`
- codebase source: `codebase/`
