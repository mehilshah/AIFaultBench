# Bug 732

This bundle reproduces the Chroma filter-conversion fault from [issue #6258](https://github.com/mem0ai/mem0/issues/6258): an unsupported operator is silently rewritten as equality instead of raising an error.  The offline repro loads the pinned checkout, calls the affected method with `betwen`, and fails after observing the incorrect equality clause.

Current result on this host: reproduced.

Files: `repro.py` is the minimal reproducer; `requirements.txt`, `setup_env.sh`, and `run_repro.sh` set up and run it; `repro_stdout.log` and `repro_stderr.log` are the captured final evidence; `reproduction.json` and `reproduction_trajectory.md` record the result.

Run:

```bash
bash run_repro.sh
```
