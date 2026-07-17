# Reproduction Trajectory — Bug 170: kornia

- **Bug report:** [https://github.com/kornia/kornia/issues/3464](https://github.com/kornia/kornia/issues/3464)
- **Repository:** kornia/kornia @ `58cc4de`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a venv and installed the runtime dependencies from requirements.txt.
2. Executed repro.py through run_repro.sh with torch.manual_seed(42), a 4-image batch, and RandomThinPlateSpline(p=1.0, same_on_batch=True).
3. Observed src_equal=True and dst_equal=False for aug._params, which violates the same_on_batch contract.
4. The script ended with an AssertionError because the destination control points differ across batch elements.

## Observed behavior

- Running bash run_repro.sh produced src_equal=True and dst_equal=False in repro_stdout.log, then repro.py failed with AssertionError: RandomThinPlateSpline should reuse identical TPS control points across the batch in repro_stderr.log.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
