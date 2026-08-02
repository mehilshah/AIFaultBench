# Bug 716

At the pinned SWE-agent revision, the open-PR hook embeds the whole agent trajectory in the pull-request body without limiting its size. `repro.py` uses an offline GitHub-client double with GitHub's 65,536-character body limit and verifies that the hook sends an oversized body, which would produce the reported HTTP 422 response.

Current result on this host: reproduced.

Files: `repro.py` is the deterministic offline reproducer; `requirements.txt`, `setup_env.sh`, and `run_repro.sh` create and run its isolated environment; `repro_stdout.log` and `repro_stderr.log` capture the final run; `reproduction.json` and `reproduction_trajectory.md` record the evidence.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
