# Reproduction Trajectory — Bug 210: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/2437](https://github.com/pytorch/rl/issues/2437)
- **Repository:** pytorch/rl @ `36545af`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a temporary scratch directory and initialize LazyMemmapStorage with that path.
2. Write a TensorDict containing keys `a` and `d`, then extend with a partial TensorDict containing only `a`.
3. Reinitialize LazyMemmapStorage with the same scratch directory.
4. Write a single-row TensorDict containing keys `a` and `d`, then extend with a partial TensorDict containing only `a`.
5. Read back `storage["d"]` and observe that rows 1 through 4 keep stale non-zero data instead of being zero-initialized.

## Observed behavior

- Running `bash run_repro.sh` on the local codebase with torch 2.4.0 and tensordict 0.5.0 produced `second_run_d = tensor([[1.],[1.],[1.],[1.],[1.],[0.]])` while the expected value was `tensor([[1.],[0.],[0.],[0.],[0.],[0.]])`. The script printed `BUG_REPRODUCED`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
