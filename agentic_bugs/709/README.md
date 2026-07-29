# Bug 709

The report says Gemini 3 Pro tool calls fail when their first function-call
message lacks `thought_signature`. The offline repro feeds precisely that
message through the pinned CAMEL Gemini request-preparation path, without an
API key or network call. On this host the pinned revision adds the fallback
`skip_thought_signature_validator`, so the reported failure is not reproduced.

Files: `repro.py` is the check; `requirements.txt` pins its dependencies;
`setup_env.sh` creates the environment; `run_repro.sh` runs it; and the log and
trajectory files record the observed result.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
