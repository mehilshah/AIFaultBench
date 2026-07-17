# Reproduction Trajectory — Bug 569: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/46762](https://github.com/huggingface/transformers/issues/46762)
- **Repository:** huggingface/transformers @ `ad697ec123f5133e5aae45c97c23d90ea52a1bd8`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Installed a CPU-compatible torch runtime in the local Python 3.11 environment.
2. Ran `bash run_repro.sh` against a synthetic tensor case shaped to make the two heads prefer different key blocks.
3. Observed the current `amax(dim=1)` collapse return one shared top block, while the per-head reference selects different blocks.

## Observed behavior

- The synthetic tensor repro shows the current reduction collapses both heads to the same block ranking: current_block_scores=[[ [10.0, 10.0] ]] and current_top1=0. The per-head reference keeps distinct rankings: head 0 selects block 0 and head 1 selects block 1.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
