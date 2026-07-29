# Bug 752

`SubQuestionQueryEngine` catches only `ValueError` while executing a sub-question, so a normal runtime failure from one tool aborts the whole query rather than allowing the remaining answers to be synthesized. The offline repro uses fake query engines and confirms that a deterministic `RuntimeError` escapes on this host; no API key, model, or runtime network call is used.

Files: `repro.py` is the reproducer; `requirements.txt`, `setup_env.sh`, and `run_repro.sh` create and run its isolated environment; `repro_stdout.log` and `repro_stderr.log` are final-run evidence; `reproduction.json` and `reproduction_trajectory.md` record the result.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
