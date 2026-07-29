# Bug 664

Bedrock Converse's streaming parser concatenates tool-use JSON fragments but puts the resulting JSON string into `ToolCallBlock.tool_kwargs` instead of a dictionary. The offline repro stubs the Bedrock event stream, checks that exact wrong type, prints it, and raises an assertion; it reproduced on this host using the released issue-era `llama-index-llms-bedrock-converse==0.14.9` package after the full repository clone did not complete.

Files: `repro.py` is the deterministic reproduction, `requirements.txt` pins its environment, `setup_env.sh` creates it, `run_repro.sh` runs it, and `repro_stdout.log`/`repro_stderr.log` are final-run evidence. `reproduction.json` and `reproduction_trajectory.md` record the result.

Run with:

```bash
bash run_repro.sh
```
