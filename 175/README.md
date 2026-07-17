# Bug 175

Reproduction bundle for Lark issue `#1416`.

Bug report summary:
- `Lark(..., parser='lalr', transformer=MyTransformer())` returns the raw token `1.0`
  instead of invoking `MyTransformer.acos_func()` and returning the expected string.
- Local checkout version: `lark 1.1.9`

Files in this folder:
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

Run locally:
```bash
bash setup_env.sh
bash run_repro.sh
```

The repro script prints the actual parse result and fails an assertion because the
transformation is not applied.
