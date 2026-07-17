# Reproduction Trajectory — Bug 206: POT

- **Bug report:** [https://github.com/PythonOT/POT/issues/691](https://github.com/PythonOT/POT/issues/691)
- **Repository:** PythonOT/POT @ `68e3926`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created isolated virtual environments for POT 0.9.4 and POT 0.9.5 with numpy==1.26.4 and scipy==1.13.1.
2. Executed the issue's sinkhorn_knopp_unbalanced example in each environment and in the local checkout.
3. Compared the resulting transport matrices and confirmed that 0.9.4 differs from 0.9.5.
4. Recorded the run output in repro_stdout.log and repro_stderr.log.

## Observed behavior

- Running the report snippet on this checkout prints POT 0.9.6dev0 with [[0.32205361, 0.11847690], [0.11847690, 0.32205361]]. A clean venv with POT==0.9.4 prints [[0.51122814, 0.18807032], [0.18807032, 0.51122814]], while POT==0.9.5 prints the same matrix as the checkout. The numerical output changed between 0.9.4 and 0.9.5.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
