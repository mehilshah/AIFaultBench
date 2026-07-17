# Bug 387

Issue reference: `https://github.com/sdv-dev/SDV/issues/2826`

What this bundle checks:
- the reported composite-primary-key path against the local SDV snapshot
- whether the public metadata API in this checkout can even reach the reported state

Current outcome:
- `SingleTableMetadata.set_primary_key(['guest_email', 'billing_address'])` is rejected with `InvalidMetadataError: 'primary_key' must be a string.`
- because of that, the reported composite-key validation bug is not reproducible in this snapshot

Run:
`bash run_repro.sh`

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
