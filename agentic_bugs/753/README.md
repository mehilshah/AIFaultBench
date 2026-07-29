# Bug 753

Bedrock Converse drops a reasoning signature when Bedrock sends it in a streaming
`reasoningContent` delta without a `text` field. The reproduction uses a fully
local recorded stream and checks that the final `ThinkingBlock` has the expected
signature; the pinned checkout instead produces an empty signature and fails.
This host reproduced the bug without an AWS request or credentials.

Files: `repro.py` is the deterministic reproducer; `requirements.txt` and
`setup_env.sh` create its environment; `run_repro.sh` is the entrypoint;
`repro_stdout.log` and `repro_stderr.log` are final-run evidence; and
`reproduction.json` and `reproduction_trajectory.md` record the result.

```bash
bash setup_codebase.sh
bash run_repro.sh
```
