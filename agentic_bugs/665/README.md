# Bug 665

`to_openai_message_dict` in the issue-era OpenAI integration copies a
`ToolCallBlock` dictionary directly into `function.arguments`, although the
OpenAI Chat Completions schema requires a JSON string. The offline repro
constructs that message and fails after verifying that the emitted arguments
are a dictionary. This host reproduced the fault using the released
issue-era packages because the full repository clone was impractically large.

Files: `repro.py` is the deterministic repro; `requirements.txt` pins its
environment; `setup_env.sh` creates it; `run_repro.sh` is the entrypoint; and
`repro_stdout.log` / `repro_stderr.log` are captured evidence.

Run:

```bash
bash run_repro.sh
```
