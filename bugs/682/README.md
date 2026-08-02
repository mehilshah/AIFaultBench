# Bug 682

The pinned Azure OpenAI providers rewrite the final caller-owned message from
`assistant` to `ai` before sending it, and call `.replace()` on multimodal
list content. The offline repro substitutes the Azure client, confirms the
caller data is mutated, and confirms both providers raise the reported
`AttributeError` for a content-block list. This host reproduces the bug.

Files: `repro.py` is the deterministic test; `requirements.txt` pins its
dependencies; `setup_env.sh` creates the environment; `run_repro.sh` is the
entrypoint; and `repro_stdout.log`/`repro_stderr.log` contain final-run
evidence.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
