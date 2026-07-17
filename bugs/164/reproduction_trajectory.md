# Reproduction Trajectory — Bug 164: kornia

- **Bug report:** [https://github.com/kornia/kornia/issues/1396](https://github.com/kornia/kornia/issues/1396)
- **Repository:** kornia/kornia @ `7700ce0`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Prepended the local `codebase/` snapshot to `sys.path` and imported `kornia.testing.tensor_to_gradcheck_var`.
2. Ran the 2D amin/amax gradcheck case from the bug report and confirmed it passes.
3. Ran the 3D amin/amax gradcheck case from the bug report and confirmed it fails with a Jacobian mismatch.

## Observed behavior

- Running the repro with the local Kornia helper shows `gradcheck_2d=True` and `gradcheck_3d_failed=GradcheckError: Jacobian mismatch for output 0 with respect to input 0`. The 3D numerical Jacobian has 0.5000 entries where the analytical Jacobian has 0.2500 entries.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
