# Bug 474

This folder contains a self-contained reproduction bundle for the Pyro import-time metaclass conflict reported in [pyro-ppl/pyro#3172](https://github.com/pyro-ppl/pyro/issues/3172).

## What reproduces

`repro.py` patches `torch.nn.ModuleList` with a class whose metaclass is incompatible with Pyro's `_PyroModuleMeta`. Importing `pyro.distributions` then fails while `pyro.infer.autoguide.guides.AutoGuideList` is being defined, raising:

`TypeError: metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases`

## Files

- `repro.py`: minimal reproducer
- `requirements.txt`: package pins
- `setup_env.sh`: creates a local venv and installs the pinned deps
- `run_repro.sh`: runs the reproducer
- `reproduction.json`: structured result
- `repro_stdout.log` / `repro_stderr.log`: captured run output

## Run

```bash
bash ./run_repro.sh > repro_stdout.log 2> repro_stderr.log
```

The exact historical PyTorch nightly from the issue report is no longer available on the public index here, so the reproducer uses a local `ModuleList` shim to drive the same import-time failure path deterministically.
