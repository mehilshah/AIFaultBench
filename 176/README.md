# Bug 176

This folder reproduces https://github.com/lark-parser/lark/issues/1434.

The bug is intermittent: the exact same grammar yields different parse trees across fresh Python processes. The repro harness runs the parser multiple times in subprocesses until it observes more than one tree shape.

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

Reproduction command:
`bash run_repro.sh`

Source summary:
- issue URL: `https://github.com/lark-parser/lark/issues/1434`
- inferred library: `lark`
- inferred library version from local checkout: `1.2.0`
