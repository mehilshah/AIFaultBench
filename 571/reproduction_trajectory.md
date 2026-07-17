# Reproduction Trajectory — Bug 571: pytorch-lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21463](https://github.com/Lightning-AI/pytorch-lightning/issues/21463)
- **Repository:** Lightning-AI/pytorch-lightning @ `027455bcd9433f201b1136f68d54b1a07588abe3`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Build a toy retrieval batch with exact sketch/gallery matches.
2. Run the user's on_validation_epoch_end metric block unchanged.
3. Observe mAP@200=0.0 and p@200=0.0.

## Observed behavior

- Perfect retrieval still reports AP=0.0 because the positive score is 0.0 and torchmetrics.retrieval_average_precision masks non-positive predictions.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
