# Bug 754

At the pinned llama_index commit, `OpenAILike.as_structured_llm()` forwards an
internally added `tool_choice="required"` to the completion endpoint even when
the model explicitly has `is_function_calling_model=False`. The offline repro
injects an OpenAI-shaped client whose completion endpoint rejects that keyword
and confirms the reported `TypeError`. The fault reproduced on this host.

Files: `repro.py` is the deterministic reproducer; `requirements.txt` and
`setup_env.sh` create the isolated environment; `run_repro.sh` is the
entrypoint; the two log files record the final run; and `reproduction.json` /
`reproduction_trajectory.md` contain the evidence and procedure.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
