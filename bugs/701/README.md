# Bug 701

This bundle reproduces a Pydantic AI message-history round-trip failure. A
`NativeToolReturnPart` can be placed in `ModelRequest` and serialized, but the
request-part discriminated union does not include its `builtin-tool-return`
tag, so revalidation of the JSON raises `ValidationError: union_tag_invalid`.
The reproduction is offline and uses no model provider or API key.

The bug reproduced on this host at the pinned commit: `run_repro.sh` exits 1
after asserting and re-raising the expected validation error.

Files:

- `repro.py` — minimal deterministic reproducer.
- `requirements.txt` — exact runtime dependency pins.
- `setup_env.sh` / `run_repro.sh` — environment setup and one-command runner.
- `repro_stdout.log` / `repro_stderr.log` — captured final-run evidence.
- `reproduction.json` / `reproduction_trajectory.md` — structured result and narrative.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
