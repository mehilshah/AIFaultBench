# Reproduction Trajectory — Bug 209: torchao

- **Bug report:** [https://github.com/pytorch/ao/issues/3490](https://github.com/pytorch/ao/issues/3490)
- **Repository:** pytorch/ao @ `ff6d9e2`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create the isolated environment with `bash setup_env.sh`.
2. Run the reproducer with `bash run_repro.sh`.
3. Observe that `quantize_(..., FqnToConfig({"l": QATConfig(..., step="prepare")}), filter_fn=None)` leaves `m.l` as `torch.nn.Linear`.

## Observed behavior

- After installing torch 2.8.0+cpu and numpy, `bash run_repro.sh` prints `before=torch.nn.modules.linear.Linear`, `after=torch.nn.modules.linear.Linear`, and `BUG: module was not swapped`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
