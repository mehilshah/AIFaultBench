# Bug 114

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
- `transformers==4.49.0` does not export `shard_checkpoint` from `transformers.modeling_utils`
- the repro is a minimal import test, not a full training run
- the run succeeds in demonstrating the reported `ImportError`

Run the repro:
`bash run_repro.sh`

Source summary:
- issue URL: `https://github.com/axolotl-ai-cloud/axolotl/issues/2387`
- commit hash: `not found in Dataset.csv`
- inferred library: `axolotl`
- inferred library version: `0.8.0.dev0`
- bug report source: `bug_report.txt`
- codebase source: `codebase`
