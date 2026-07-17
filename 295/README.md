# Bug 295

Repro bundle for https://github.com/sdv-dev/SDV/issues/2868.

Observed behavior:
- `sdv._utils.get_possible_chars('(ab)*')` returns `['ab']` under `rdt==1.21.0`.
- The legacy unit test expected `ValueError: REGEX operation: SUBPATTERN is not supported by SDV.`
- That expectation no longer holds, which matches the bug report.

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

Reproduction command:
`bash setup_env.sh && bash run_repro.sh`
