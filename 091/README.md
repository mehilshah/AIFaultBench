# x-transformers issue 271 repro

This bundle reproduces the `model.generate` failure reported in:
`https://github.com/lucidrains/x-transformers/issues/271`

## What fails

Running the reproduction script on the local `codebase/` snapshot raises:

`RuntimeError: The size of tensor a (258) must match the size of tensor b (30) at non-singleton dimension 3`

The error happens during decoder cross-attention inside `generate()`.

## Files

- `repro.py`: minimal CPU-only reproducer.
- `requirements.txt`: pinned runtime dependencies.
- `setup_env.sh`: creates `.venv` and installs dependencies.
- `run_repro.sh`: runs the repro and writes `repro_stdout.log` / `repro_stderr.log`.

## Run

```bash
bash run_repro.sh
```
