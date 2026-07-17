# SliceSampler slowdown repro

This bundle reproduces the performance bug reported in `bug_report.txt`:
adding `SliceSampler` to a `ReplayBuffer` makes repeated `sample()` calls much slower.

## Files

- `repro.py` runs the benchmark and prints the slowdown factor.
- `setup_env.sh` creates a local virtualenv and installs the needed runtime deps.
- `run_repro.sh` bootstraps the env and executes the benchmark.
- `manifest.json` summarizes the bundle.

## Run

```bash
bash run_repro.sh
```

Expected output includes timing for the baseline and `SliceSampler` cases, plus a slowdown factor around 25x on this snapshot.

## Compatibility note

The current checkout still imports deprecated `tensordict` names. `repro.py` installs a small compatibility shim before importing TorchRL so the benchmark can run against modern `tensordict` releases.
