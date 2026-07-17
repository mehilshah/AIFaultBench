# Reproduction Trajectory — Bug 348: pytorch-lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21703](https://github.com/Lightning-AI/pytorch-lightning/issues/21703)
- **Repository:** Lightning-AI/pytorch-lightning @ `78bf0214a0ad7571391619dca952c13988c0dc51`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a clean venv with the CPU torch wheel and Lightning's minimal runtime dependencies.
2. Ran `repro.py` from a real file so `multiprocessing_context='spawn'` works.
3. Observed `Trainer.predict()` fail during teardown in `CombinedLoader.reset()` after the first batch.

## Observed behavior

- Running `./run_repro.sh` on the local source tree with `torch 2.9.1+cpu` and `workers=4` exits non-zero. stderr shows Lightning tearing down prediction through `CombinedLoader.reset()` -> `_shutdown_workers_and_reset_iterator()` -> `dataloader._iterator._shutdown_workers()`, which raises `RuntimeError: DataLoader worker ... is killed by signal: Aborted`, followed by the secondary `RuntimeError: Please call `iter(combined_loader)` first.`

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./setup_env.sh && ./run_repro.sh
```
