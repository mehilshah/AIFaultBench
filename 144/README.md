# Bug 144

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

Repro summary:
- `CrossEncoder.__init__` records the target device but does not move the model onto it.
- `predict()` does call `self.model.to(self._target_device)`.
- The repro uses a local fake model/tokenizer so it runs offline and isolates the control flow.

Run:
`bash ./run_repro.sh`

Source summary:
- issue URL: `https://github.com/huggingface/sentence-transformers/issues/3078`
- commit hash: `not found in Dataset.csv`
- inferred library: `sentence-transformers`
- inferred library version: `3.4.0.dev0`
- bug report source: `bug_report.txt`
- codebase source: `codebase`
