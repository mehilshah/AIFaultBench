# Bug 328

Reproduction bundle for POT issue 24: `ot.da.OTDA().fit(a, b)` returns a transport plan whose total mass is below `1.0`.

What this folder contains:
- `bug_report.txt`: original issue report
- `codebase/`: local POT source snapshot
- `repro.py`: standalone reproduction entrypoint
- `compat_shims.py`: runtime compatibility aliases for modern SciPy/NumPy
- `requirements.txt`: bundle dependencies
- `setup_env.sh`: creates the venv and builds the local extension in place
- `run_repro.sh`: one-shot runner that records stdout/stderr
- `reproduction.json`: machine-readable result
- `repro_stdout.log`, `repro_stderr.log`: captured output from the last run

Verified local result:
- `sum(opt.G) = 0.7333999999999999`
- expected value from the report: `1.0`

Run the repro:
```bash
./run_repro.sh
```
