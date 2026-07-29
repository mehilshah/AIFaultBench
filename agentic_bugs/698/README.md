# Bug 698

At the pinned smolagents commit, `CodeAgent.__init__` validates `executor_type` before it calls the overridable `create_python_executor()` method. The offline reproduction subclasses `CodeAgent`, supplies `"my_executor"`, and verifies the exact `ValueError` is raised before the custom factory runs. This host reproduces the bug: `run_repro.sh` exits with status 1 and prints the observed fault.

Files: `repro.py` contains the minimal assertion, `requirements.txt` pins runtime dependencies, `setup_env.sh` builds the environment, `run_repro.sh` is the entrypoint, and `repro_stdout.log`/`repro_stderr.log` capture the final run. `reproduction.json` and `reproduction_trajectory.md` record the evidence.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
