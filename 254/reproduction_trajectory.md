# Reproduction Trajectory — Bug 254: torchtitan

- **Bug report:** [https://github.com/pytorch/torchtitan/issues/1626](https://github.com/pytorch/torchtitan/issues/1626)
- **Repository:** pytorch/torchtitan @ `cd337db`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated venv with sh setup_env.sh.
2. Ran sh run_repro.sh, which loads codebase/torchtitan/components/dataloader.py and triggers the empty-dataloader path.
3. Observed RuntimeError: generator raised StopIteration instead of catching DataloaderStopIteration.

## Observed behavior

- repro_stdout.log shows DataloaderStopIteration is a subclass of StopIteration and the empty-data generator raises RuntimeError: generator raised StopIteration. The repro exited with status 1.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
sh run_repro.sh
```
