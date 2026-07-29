# Bug 676

At the pinned DSPy checkout, `UsageTracker` converts two successive `None`
usage-detail values into integer `0`. A following usage entry containing a
detail dictionary then triggers `TypeError: object of type 'int' has no len()`.
The deterministic repro calls that internal aggregation path directly, with no
LLM, API key, MLflow server, or network request. The fault reproduces on this
host.

Files:

- `repro.py` — deterministic failing case.
- `requirements.txt`, `setup_env.sh`, `run_repro.sh` — environment and entrypoint.
- `repro_stdout.log`, `repro_stderr.log`, `reproduction.json`, and
  `reproduction_trajectory.md` — observed evidence and metadata.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
