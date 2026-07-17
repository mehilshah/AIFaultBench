# Bug 483

This folder contains the standardized reproduction bundle for the reported `auto_docstring` stdout leak.

Reused inputs:
- `bug_report.txt`
- `codebase/`

Generated artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Observed result:
- The reported import-time diagnostics did not reproduce on this snapshot.
- `run_repro.sh` completes without emitting the `[ERROR]` doc-lint lines described in the issue.

Source summary:
- issue URL: `https://github.com/huggingface/transformers/issues/46877`
- commit hash: `9b6af5d77de78f0a57a098b2809009ad6ec0cfe3`
- library: `transformers`
- report version: `5.13.0.dev0`
