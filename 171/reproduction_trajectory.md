# Reproduction Trajectory — Bug 171: kornia

- **Bug report:** [https://github.com/kornia/kornia/issues/996](https://github.com/kornia/kornia/issues/996)
- **Repository:** kornia/kornia @ `bd49f1b`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. bash setup_env.sh
2. bash run_repro.sh
3. Observed one passing input shape and two failing input shapes from the bug report

## Observed behavior

- projections_from_fundamental(torch.randn(1, 3, 3)) returns shape [1, 3, 4, 2], while torch.randn(1, 1, 3, 3) raises AssertionError: torch.Size([1, 1, 3]) and torch.randn(3, 3) raises AssertionError: torch.Size([3]).

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
