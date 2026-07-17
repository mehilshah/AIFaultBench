# Reproduction Trajectory — Bug 166: kornia

- **Bug report:** [https://github.com/kornia/kornia/issues/2822](https://github.com/kornia/kornia/issues/2822)
- **Repository:** kornia/kornia @ `bbf4b59`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Set PYTHONPATH to include the local codebase checkout.
2. Run repro.py with torch.manual_seed(42).
3. Compute x * x, x[0] * x[0], x[[0,0,0]] * x, and x[[0,1,2]] * x.
4. Observe that a[0] matches b, but c[0] does not match d[0].

## Observed behavior

- Running bash run_repro.sh reproduces the issue: the script prints a[0] == b : True and c[0] == d[0]: False, and stderr shows the torch.cross deprecation warning from codebase/kornia/geometry/quaternion.py:128. The repro exits with status 1 after detecting the mismatch.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
