# Bug 713

This bundle reproduces the custom-component loader fault from [langflow issue #12775](https://github.com/langflow-ai/langflow/issues/12775): `from module import Name as Alias` places `Name`, rather than `Alias`, in its execution scope. The repro loads the pinned validator source offline with tiny import-only stubs, asserts the resulting `NameError`, and exits non-zero when the bug is present. On this host, the pinned commit reproduced the fault with `AliasedName` undefined.

Files: `repro.py` is the deterministic repro; `requirements.txt`, `setup_env.sh`, and `run_repro.sh` provision and run it; `repro_stdout.log` and `repro_stderr.log` contain final-run evidence; `reproduction.json` and `reproduction_trajectory.md` record the result.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
