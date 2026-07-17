# Bug 178

This folder contains a minimal reproduction for:
`https://github.com/lark-parser/lark/issues/1569`

Observed behavior in this checkout:
`Lark(..., lexer="basic")` crashes when lexing with a terminal regex that starts with an inline flag such as `/(?s)./`.

Reproduction:
`bash run_repro.sh`

Files in this bundle:
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
