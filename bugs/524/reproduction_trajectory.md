# Reproduction Trajectory — Bug 524: deepspeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7752](https://github.com/deepspeedai/DeepSpeed/issues/7752)
- **Repository:** microsoft/DeepSpeed @ `b4e74a918bef25ffd13c9756d80aaef5ee17f94a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Install the local codebase in a clean virtual environment with torch 2.7.1+cpu.
2. Run ./run_repro.sh from the standardized folder.
3. Observe BF16_Optimizer.destroy() raising IndexError when DummyOptim leaves bf16_groups empty.

## Observed behavior

- codebase/deepspeed/runtime/bf16_optimizer.py:105-111 unconditionally indexes self.bf16_groups[i] during destroy().
- run_repro.sh produced repro_stdout.log showing "constructed=BF16_Optimizer bf16_groups=0" followed by "BUG REPRODUCED: IndexError: list index out of range".
- run_repro.sh exited with status 1, and repro_exit_code.txt contains 1.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
