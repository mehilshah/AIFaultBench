# Bug 623 Reproduction

This bundle reproduces the `TypeError: 'numpy.float64' object cannot be interpreted as an integer` reported in Lightning issue 21429.

The failure is triggered in Asteroid's `LibriMix.__getitem__`, where `random.randint` receives a NumPy float derived from the `length` column in MiniLibriMix metadata.

## What the repro does

1. Creates a tiny synthetic MiniLibriMix-style metadata directory.
2. Loads `asteroid.data.librimix_dataset.LibriMix` directly from the installed Asteroid source tree.
3. Monkeypatches `LibriMix.mini_from_download` so `LibriMix.loaders_from_mini(...)` uses the synthetic fixture.
4. Iterates the first batch, which raises the TypeError in `random.randrange`.

## Files

- `repro.py`: the minimal reproducer
- `requirements.txt`: base runtime dependencies
- `setup_env.sh`: builds the local venv and installs dependencies
- `run_repro.sh`: runs the reproducer and captures stdout/stderr
- `reproduction.json`: machine-readable result

## Reproduction

```bash
bash setup_env.sh
bash run_repro.sh
```

The expected failure is:

```text
TypeError: 'numpy.float64' object cannot be interpreted as an integer
```

## Notes

- The local Lightning checkout in `codebase/` was used to confirm the issue context.
- The actual crash is in Asteroid's LibriMix dataset loader, not in Lightning's trainer code.
