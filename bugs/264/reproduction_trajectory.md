# Reproduction Trajectory — Bug 264: tinygrad

- **Bug report:** [https://github.com/tinygrad/tinygrad/issues/13853](https://github.com/tinygrad/tinygrad/issues/13853)
- **Repository:** tinygrad/tinygrad @ `9b4de8a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run `bash run_repro.sh` from the standardized bug folder.
2. The script imports the local `codebase/` via `PYTHONPATH` and executes the exact tensor sequence from the bug report.
3. Observe the mismatched shard/shrink results in `repro_stdout.log`.

## Observed behavior

- On the provided codebase, the reported script prints T.tolist()=[0, 1, 2, 3], then returns [0, 1] for shard(('CPU:0', 'CPU:1'), 0).realize().shrink(((2, 4),)) and [0, 0] for shard(('CPU:1', 'CPU:2'), 0).realize().shrink(((0, 2),)), instead of the expected [2, 3] and [0, 1].

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
