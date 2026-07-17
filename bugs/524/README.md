# DeepSpeed BF16 destroy repro

This bundle reproduces the `IndexError` reported in DeepSpeed issue 7752.

The repro avoids a full multi-process launch by installing a fake single-rank DeepSpeed comm backend, then constructing `BF16_Optimizer` around `DummyOptim` and calling `destroy()`.

## Files

- `repro.py`: minimal Python repro
- `requirements.txt`: runtime dependencies
- `setup_env.sh`: creates `.venv` and installs dependencies
- `run_repro.sh`: runs the repro and writes `repro_stdout.log` and `repro_stderr.log`

## Run

```bash
./setup_env.sh
./run_repro.sh
```

Expected result:

- `repro.py` prints `BUG REPRODUCED: IndexError: list index out of range`
- `run_repro.sh` exits with status `1`
