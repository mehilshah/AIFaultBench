# Bug 440

Deepcopy does not preserve `LoraConfig.r` in this `peft` snapshot.

## Repro

1. Run `bash setup_env.sh`
2. Run `bash run_repro.sh`

Expected: the copied adapter keeps `r=87`.

Observed: the copied adapter falls back to the default `r=8`, and `repro.py` raises `AssertionError`.
