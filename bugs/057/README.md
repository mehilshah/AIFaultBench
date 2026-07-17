# Bug 057

Reproduction bundle for Keras issue 1665.

Bug report summary:
- The example `examples/nlp/neural_machine_translation_with_transformer.py` imports `from keras import ops`.
- In a Keras 2.14 runtime, that import fails with `ImportError: cannot import name 'ops' from 'keras'`.

Included artifacts:
- `bug_report.txt`
- `codebase/`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Usage:
1. Run `bash setup_env.sh`
2. Run `bash run_repro.sh`
3. Inspect `repro_stdout.log` and `repro_stderr.log`

The repro intentionally stops at the failing import and does not download data or train the model.
