# Bug 688

`ChatPerplexity._convert_message_to_dict` in the issue-era
`langchain-perplexity==1.3.1` drops an `AIMessage`'s `tool_calls` and cannot
serialize a `ToolMessage`. The offline repro checks both outcomes directly;
it does not create a provider request or require an API key. The fault
reproduces on this host.

Files:

- `repro.py` — deterministic offline fault check
- `requirements.txt` — fully pinned package environment
- `setup_env.sh` — creates the virtual environment and installs dependencies
- `run_repro.sh` — reproduction entrypoint
- `repro_stdout.log` / `repro_stderr.log` — final-run evidence
- `reproduction.json` / `reproduction_trajectory.md` — recorded verdict and method

Run:

```bash
bash run_repro.sh
```
