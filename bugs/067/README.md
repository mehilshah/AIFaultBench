# Bug 067

This folder is the reusable standardized benchmark input for this bug.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/`

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction command:
`bash run_repro.sh`

Verdict:
- `reproducible`: `false`
- `reason`: TensorFlow 2.16.1 accepts `(batch, h, w, 1)` labels for sparse categorical crossentropy and returns the same loss as the squeezed `(batch, h, w)` labels.

Source summary:
- issue URL: `https://github.com/keras-team/keras-io/issues/1147`
- commit hash: `54392950c4142c96ccc0f8dfd4a9a586edbe5cf2`
- inferred library: `keras-io`
- inferred library version: `2.10.0` reported in the issue body
- bug report source: `bug_report.txt`
- codebase source: `codebase/`
