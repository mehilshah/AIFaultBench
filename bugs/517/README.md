# TraceEnum_ELBO RSS Growth Repro

This bundle reproduces the memory growth reported in pyro issue 3068 using the
local `codebase/` checkout and the tutorial-style GMM model from
`codebase/tutorial/source/gmm.ipynb`.

## What the repro does

- Builds the GMM model with `AutoDelta` globals and an enumerated local
  assignment guide.
- Runs the same model/guide under `Trace_ELBO` as a control.
- Runs the same model/guide under `TraceEnum_ELBO` and measures current RSS
  from `/proc/self/status`.
- Writes the schema result to `reproduction.json`.

## Notes

- This checkout imports `pyro` through a Torch 1.x assertion. The repro script
  patches `torch.__version__` before importing `pyro` so it can run against the
  installed Torch build in this environment.
- The observed behavior on this machine was:
  - `Trace_ELBO`: RSS stayed flat after the initial allocator jump.
  - `TraceEnum_ELBO`: RSS kept increasing across later iterations.

## Run

```bash
bash run_repro.sh
```
