# Bug 738

Phoenix's Bedrock playground client forwards a raw tool specification without
the required `toolSpec` envelope. The repro builds that request from the pinned
checkout and uses botocore's local validator to confirm the resulting
`ParamValidationError`; the transport is explicitly blocked, so it never calls
AWS. The fault reproduces on this host.

Files: `repro.py`, `requirements.txt`, `setup_env.sh`, `run_repro.sh`,
`repro_stdout.log`, `repro_stderr.log`, and `reproduction.json`.

Run it with:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
