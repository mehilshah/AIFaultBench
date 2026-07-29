# Bug 758

This reproduces [smolagents issue #1674](https://github.com/huggingface/smolagents/issues/1674): the Bedrock model parser raises `KeyError` when a DeepSeek-style response places a `reasoningContent` block after its text block. `repro.py` supplies a simulated response through a fake client, so it makes no AWS, LLM-provider, or other runtime network calls. The bug reproduced on this host at the pinned commit.

Files: `repro.py` is the deterministic trigger; `requirements.txt` and `setup_env.sh` create the environment; `run_repro.sh` is the entrypoint; `repro_stdout.log` and `repro_stderr.log` are final-run evidence; and `reproduction.json` and `reproduction_trajectory.md` record the result.

```bash
bash setup_codebase.sh
bash run_repro.sh
```
