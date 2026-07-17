# Bug 042

This folder reproduces lucidrains/imagen-pytorch issue 378.

Observed failure:
- `from imagen_pytorch import Unet, Imagen`
- with `beartype==0.18.0`
- raises `BeartypeDecorHintParamDefaultViolation` during import

Files:
- `bug_report.txt`: original issue report
- `codebase/`: local checkout used for reproduction
- `repro.py`: minimal import reproducer
- `requirements.txt`: pinned runtime dependencies
- `setup_env.sh`: creates the isolated environment
- `run_repro.sh`: runs the repro and writes logs
- `reproduction.json`: schema-constrained result
- `repro_stdout.log`, `repro_stderr.log`: captured command output

Run:
```bash
bash run_repro.sh
```
