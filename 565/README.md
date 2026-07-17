# Bug 565 Reproduction

This bundle reproduces the Pyro GPU memory leak described in `bug_report.txt`.

The working repro uses the local `codebase/` snapshot with a runtime shim for the
Pyro 1.x Torch version check. On this machine the leak shows up on the
model-enumeration path:

- `torch.cuda.memory_allocated()` grows from `1536` to `103424` bytes over `200`
  `SVI.step()` calls.
- The increase is monotonic (`ups=199`).

## Run

```bash
bash run_repro.sh
```

`run_repro.sh` will create `.venv/` if needed, install the pinned dependencies,
and execute `repro.py`.

## Notes

- The repro is intentionally small and uses synthetic data.
- The local Pyro source expects Torch 1.x, so `repro.py` patches
  `torch.__version__` before importing `pyro`.
- The observed leak is on the discrete model-site enumeration path, which is
  consistent with the upstream TraceEnum_ELBO fix mentioned in the issue
  history.
