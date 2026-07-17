# Bug 235

This folder is the reusable standardized benchmark input for this bug.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/`

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Source summary:
- issue URL: `https://github.com/patrick-kidger/equinox/issues/791`
- inferred library: `equinox`
- inferred library version: `0.11.4`
- bug report source: `bug_report.txt`
- codebase source: `codebase`

Run the repro locally:

```bash
./setup_env.sh
./run_repro.sh
```

The reproduction is successful if `Foo().moo()` prints `__getattr__` hits for
`__name__` and `__qualname__`, then exits with status `1`.
