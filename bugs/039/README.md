# Bug 039 Reproduction

This folder contains a self-contained reproduction bundle for the RoPE bug described in `bug_report.txt`.

What is included:
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

Reproduction summary:
- issue URL: `https://github.com/labmlai/annotated_deep_learning_paper_implementations/issues/215`
- affected file: `codebase/labml_nn/transformers/rope/__init__.py`
- symptom: `RuntimeError` from mismatched RoPE cache shape

Run:
`bash run_repro.sh`
