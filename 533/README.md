# Reproduction Bundle

This folder reproduces the Lightning bug described in `bug_report.txt`.

## What it does

`repro.py` defines a minimal `LightningModule` that:

1. disables automatic optimization,
2. calls `self.toggle_optimizer(self.optimizers())` inside `training_step`,
3. wraps the model with `torch.compile()`, and
4. runs `Trainer.fit()` on a tiny in-memory dataset.

On the current checkout, the first training step fails during the compiled `toggle_optimizer` path.
In this environment, the traceback ends in `torch._dynamo.utils.tuple_iterator_getitem` with
`IndexError: tuple index out of range`.

## Run locally

```bash
./setup_env.sh
./run_repro.sh
```

The scripts write the program output to:

- `repro_stdout.log`
- `repro_stderr.log`

## Files

- `bug_report.txt`: source issue report
- `codebase/`: local Lightning source snapshot
- `repro.py`: standalone reproduction
- `requirements.txt`: minimal runtime dependencies
- `setup_env.sh`: creates the virtual environment and installs dependencies
- `run_repro.sh`: executes the repro and captures logs
- `manifest.json`: bundle metadata
