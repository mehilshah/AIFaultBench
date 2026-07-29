# Bug 661

CrewAI's A2A update path imports the removed `A2AClientHTTPError` symbol when it
is used with `a2a-sdk==1.0.1`. The repro constructs `A2AClientConfig` from the
pinned checkout and verifies that this local, pre-network initialization raises
the reported `ImportError`. On this host, the bug is reproduced (the script
exits 1 after printing the observed fault).

Files: `repro.py` is the offline reproducer; `requirements.txt` pins its
dependencies; `setup_env.sh` creates the environment; `run_repro.sh` runs it;
and `repro_stdout.log`/`repro_stderr.log` contain the final captured evidence.

```bash
bash setup_codebase.sh
bash run_repro.sh
```
