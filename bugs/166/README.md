# Bug 166

Quaternion multiplication in `kornia.geometry.quaternion.Quaternion` is sensitive to the input tensor shape when `Tensor.cross` is used without an explicit `dim`.

## Repro

Run:

```bash
bash run_repro.sh
```

Expected:

- `a[0] == b`
- `c[0] == d[0]`

Observed in this snapshot:

- `a[0] == b` is `True`
- `c[0] == d[0]` is `False`
- PyTorch emits a deprecation warning for `torch.cross` from `codebase/kornia/geometry/quaternion.py:128`

## Files

- `repro.py`: minimal Python reproduction.
- `requirements.txt`: minimal runtime dependencies.
- `setup_env.sh`: installs the Python dependencies.
- `run_repro.sh`: runs the reproduction against the local checkout.
- `reproduction.json`: machine-readable reproduction result.
