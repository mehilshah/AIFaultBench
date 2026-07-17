# Bug 185

Reproduction target:
`mo.ui.tabs({})` raises `IndexError` in `codebase/marimo/_plugins/ui/_impl/tabs.py`.

How to run:
`bash run_repro.sh`

What the repro does:
1. Creates a local virtualenv.
2. Installs the core runtime dependencies from `requirements.txt`.
3. Runs `repro.py` with `PYTHONPATH=codebase`.
4. Captures stdout and stderr in `repro_stdout.log` and `repro_stderr.log`.

Source summary:
`bug_report.txt`
`codebase/`

Issue URL:
`https://github.com/marimo-team/marimo/issues/7767`
