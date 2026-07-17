# Bug 220

This folder is a self-contained repro bundle for
`https://github.com/tensorflow/datasets/issues/5397`.

What is included:
- `bug_report.txt`
- `codebase/`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Current status:
- The exact upstream URL from the report now returns HTTP 403 in this
  environment.
- `repro.py` therefore uses a tiny local archive and the checked-in
  `plant_leaves` checksum metadata to exercise the same TFDS
  `NonMatchingChecksumError` path deterministically.

Run:
`./run_repro.sh`

Source summary:
- issue URL: `https://github.com/tensorflow/datasets/issues/5397`
- library: `tensorflow-datasets`
- library version: `4.9.4+nightly` in this codebase snapshot
