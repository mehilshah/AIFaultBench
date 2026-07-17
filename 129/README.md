# Ax homepage sample repro

This bundle reproduces the bug reported for the Ax homepage sample code.

## What fails

The sample imports `Client` and `RangeParameterConfig`, but then uses `ParameterType.FLOAT` without importing `ParameterType`.

## Reproduce

```bash
bash setup_env.sh
bash run_repro.sh
```

## Expected result

The script raises `NameError: ParameterType is not defined`.

## Evidence

The local checkout also contains the same stale snippet in `codebase/README.md`.
