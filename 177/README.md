# Bug 177 Repro Bundle

This folder contains a minimal reproduction for Lark issue 1457.

Observed behavior:
- `Transformer` methods decorated with `@v_args(inline=True)` receive inline children.
- `Visitor` methods decorated with the same class-level decorator still receive a single `Tree` argument, which causes a signature mismatch when the callback expects inline children.

Files:
- `repro.py`: standalone reproducer
- `run_repro.sh`: executes the reproducer
- `setup_env.sh`: installs the local bundle requirements
- `requirements.txt`: dependency list for the repro environment
- `manifest.json`: bundle metadata
- `reproduction.json`: machine-readable repro result

Run:
```bash
bash setup_env.sh
bash run_repro.sh
```
