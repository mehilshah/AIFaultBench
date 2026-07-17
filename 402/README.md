# Bug 402

Reproduction bundle for SDV issue 2825.

Observed result in this checkout:
- `Metadata.set_primary_key(['user_id', 'user_id'], table_name='accounts')` fails immediately with `InvalidMetadataError: 'primary_key' must be a string.`
- The reported `AttributeError: 'DataFrame' object has no attribute 'dtype'` is not reachable in this source snapshot.

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

Run:
`bash setup_env.sh && bash run_repro.sh`
