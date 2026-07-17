# Bug 509

This folder contains a self-contained repro for Pyro issue `#3143`.

Observed behavior in this checkout:
- first `MCMC.run()` succeeds
- second `MCMC.run()` on the same instance fails when `num_chains=2` and `mp_context='spawn'`

Files:
- `repro.py`: minimal script that triggers the failure
- `requirements.txt`: pinned runtime dependencies
- `setup_env.sh`: creates a local virtualenv and installs dependencies
- `run_repro.sh`: runs the repro and captures `repro_stdout.log` / `repro_stderr.log`
- `reproduction.json`: machine-readable result for the benchmark harness

Run:
```bash
bash run_repro.sh
```
