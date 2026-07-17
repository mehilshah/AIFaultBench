# Bug 463

Repro for JAX issue https://github.com/jax-ml/jax/issues/38268.

Observed here:
- `isinstance(x, Array)` prints `True`
- `isinstance(x, ArrayLike)` prints `False`

This matches the buggy cluster output in the report.

## Layout
- `bug_report.txt`: recovered issue report
- `codebase/`: JAX checkout at `5073cd4d871bd39a04a75aef1db21e065b903f1a`
- `repro.py`: minimal probe
- `requirements.txt`: pinned repro dependencies
- `setup_env.sh`: create and populate a local virtualenv
- `run_repro.sh`: execute the probe
- `repro_stdout.log` / `repro_stderr.log`: captured output from the probe

## Run
```bash
bash setup_env.sh
bash run_repro.sh
```
