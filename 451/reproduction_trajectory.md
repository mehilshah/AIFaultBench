# Reproduction Trajectory — Bug 451: pytorch-lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21580](https://github.com/Lightning-AI/pytorch-lightning/issues/21580)
- **Repository:** Lightning-AI/pytorch-lightning @ `283ce7733ec23786d41751f185093eac83c0ef8d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Checked out Lightning commit 283ce7733ec23786d41751f185093eac83c0ef8d.
2. Installed the Lightning CLI dependencies in an isolated virtual environment.
3. Parsed a trainer config containing FSDPStrategy with device_mesh set to [1, 4].
4. Observed SystemExit 2 with parser validation failure for tuple length 1 instead of 2.

## Observed behavior

- LightningArgumentParser rejected trainer.strategy.device_mesh=[1, 4] with the nested error 'Expected a tuple with 1 elements' for FSDPStrategy, matching the reported type-hint mismatch.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
