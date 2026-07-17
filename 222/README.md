# Bug 222

This folder is the reusable standardized reproduction bundle for Towhee issue 2714.

What is included:
- `bug_report.txt`
- `codebase/`
- generated repro artifacts in this folder

Generated files:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Repro command:
```bash
bash run_repro.sh
```

Observed result:
- constructing `towhee.serve.triton.pipeline_client.Client` fails immediately
- traceback ends at `aiohttp.connector.py` with `RuntimeError: no running event loop`
- the failure is triggered from `codebase/towhee/serve/triton/pipeline_client.py`

Notes:
- the repro loads the local `pipeline_client.py` directly
- it uses a tiny namespace-package shim so unrelated `towhee/__init__.py` imports do not mask the bug
