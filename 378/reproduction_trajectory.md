# Reproduction Trajectory — Bug 378: lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21692](https://github.com/Lightning-AI/pytorch-lightning/issues/21692)
- **Repository:** Lightning-AI/pytorch-lightning @ `0e20e15f2376f4f356470b08875639a945c43334`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Inspected the bug report and the local source tree.
2. Checked the local package for the malicious `_runtime` import chain described upstream.
3. Ran the generated repro script against the checked-in source tree.

## Observed behavior

- Running `bash run_repro.sh` produced `{\n  "findings": [],\n  "local_version": "2.6.2",\n  "router_js_exists": false,\n  "runtime_dir_exists": false,\n  "start_py_exists": false\n}` followed by `Result: not reproducible in this checkout`.
- The local checkout does not contain `codebase/src/lightning/_runtime`, `start.py`, or `router_runtime.js`.
- `codebase/src/lightning/__init__.py` only imports the public API; it does not spawn a background thread or subprocess on import.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

This workspace only contains the clean source checkout; the malicious PyPI wheel artifacts described in the upstream report are not present here, and the affected releases are no longer available from the public index in this environment.
