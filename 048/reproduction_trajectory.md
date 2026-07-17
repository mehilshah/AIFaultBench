# Reproduction Trajectory — Bug 048: fairseq

- **Bug report:** [https://github.com/facebookresearch/fairseq/issues/5123](https://github.com/facebookresearch/fairseq/issues/5123)
- **Repository:** facebookresearch/fairseq @ `af12c9c6407bbcf2bca0b2f1923cf78f3db8857c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Execute the self-contained sliding-window reproducer in `repro.py`.
2. Observe the first two emission tensors being produced with different time lengths.
3. Hit the concatenation failure at the `fake_cat(..., dim=1)` step.

## Observed behavior

- Running `bash run_repro.sh` prints the sliding-window frame counts `1649` and `1799` for the first two windows and then fails with `RuntimeError: Sizes of tensors must match except in dimension 1. Expected size 1649 but got size 1799 for tensor number 1 in the list.`

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
