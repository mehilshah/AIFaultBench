# Reproduction Trajectory — Bug 308: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/3870](https://github.com/pytorch/rl/issues/3870)
- **Repository:** pytorch/rl @ `52cf596100dc2d0e6d678835fe05d88dc8584fd9`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local venv with torch 2.5.1+cpu, tensordict 0.13.0, and pyvers.
2. Imported the local codebase via PYTHONPATH and constructed ReplayBuffer(storage=ListStorage(max_size=100), batch_size=2, prefetch=1).
3. Extended the buffer with torch.arange(100), called sample(), and inspected len(rb._prefetch_queue).
4. Observed len(rb._prefetch_queue) == 0 instead of the expected 1, which triggers the assertion.

## Observed behavior

- Running bash run_repro.sh prints torch=2.5.1+cpu and prefetch_queue_length=0, then fails with AssertionError: Bug present: Expected prefetch queue to have 1 item, but got 0.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
