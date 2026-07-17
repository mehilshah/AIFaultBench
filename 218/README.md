# Bug 218

This folder contains a minimal repro for Stanza issue 1366.

Reproduction command:
`./run_repro.sh`

What it demonstrates:
The sentence-level `to_dict()` output includes a multi-word-token dictionary that does not have an `xpos` key. Indexing `entry["xpos"]` on that dict raises `KeyError: 'xpos'`.

Files of interest:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Inputs preserved from the benchmark:
- `bug_report.txt`
- `codebase/`
