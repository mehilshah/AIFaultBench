# Bug 733

`mem0-cli` violates `set_nested_value()`'s boolean failure contract when a
non-numeric value is assigned to the integer `version` config field: it raises
an uncaught `ValueError`. The offline repro imports the pinned CLI checkout and
asserts that exact exception and message. On this host, the bug reproduces.

Files: `repro.py` is the minimal trigger; `requirements.txt` and
`setup_env.sh` create the isolated environment; `run_repro.sh` is the
entrypoint; `repro_stdout.log` and `repro_stderr.log` contain final-run
evidence; `reproduction.json` and `reproduction_trajectory.md` record the
result.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
