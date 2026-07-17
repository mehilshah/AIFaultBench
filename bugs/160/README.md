# Bug 160

This folder contains a standalone reproduction bundle for the `Point` equality bug reported in:
`https://github.com/influxdata/influxdb-client-python/issues/623`

Reused inputs:
- `bug_report.txt`
- `codebase/`

Generated reproduction artifacts:
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

Observed behavior:
- two `Point` objects with identical measurement, tags, fields, and timestamp serialize to the same line protocol
- the same objects compare unequal with `==`
