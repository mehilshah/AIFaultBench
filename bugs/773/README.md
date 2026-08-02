# Bug 773

At browser-use 0.12.1, `session_to_python_script` accepts an object annotated as `CodeAgent` but does not validate it. Passing the issue's regular `Agent` causes its direct `agent.session.cells` access to fail with `AttributeError`. The offline repro constructs a real `Agent` with a model double and confirms that exact fault on this host; it exits 1 when the behavior is present.

Files: `repro.py` is the deterministic reproducer; `requirements.txt`, `setup_env.sh`, and `run_repro.sh` create and run the isolated environment; `repro_stdout.log` and `repro_stderr.log` are captured evidence; `reproduction.json` and `reproduction_trajectory.md` record the result.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
