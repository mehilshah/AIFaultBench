# Bug 684

Langflow 1.11.0 indirectly imports `mem0ai==2.0.12`, whose import-time setup
unconditionally creates `~/.mem0`.  On a read-only application home this
prevents Langflow from starting before it can serve requests. The repro sets
`HOME` to a real read-only mount on this host and checks that the import raises
the reported `OSError: [Errno 30] Read-only file system`.

Current result on this host: reproduced.

Files: `repro.py` is the deterministic check; `requirements.txt` pins the
issue-era dependency graph; `setup_env.sh` creates the environment;
`run_repro.sh` runs it; `repro_stdout.log` and `repro_stderr.log` are final-run
evidence; `reproduction.json` is the machine-readable result; and
`reproduction_trajectory.md` records the investigation.

Run:

```bash
bash run_repro.sh
```
