# Bug 653

At the pinned CAMEL commit, the AWS Bedrock Converse message converter emits a separate `user` message for each tool result after an assistant emits multiple tool calls. Bedrock requires every pending `toolResult` block in one immediately following user message. The offline repro constructs that payload without credentials or a network call and exits non-zero after observing the invalid sequence on this host.

Files: `repro.py` is the deterministic reproducer; `requirements.txt`, `setup_env.sh`, and `run_repro.sh` create and run the isolated environment; `repro_stdout.log` and `repro_stderr.log` capture the final evidence; `reproduction.json` and `reproduction_trajectory.md` record the result.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
