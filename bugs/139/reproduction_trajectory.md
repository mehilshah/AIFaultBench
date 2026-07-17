# Reproduction Trajectory — Bug 139: timm

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2282](https://github.com/huggingface/pytorch-image-models/issues/2282)
- **Repository:** huggingface/pytorch-image-models @ `6ab2af6`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtual environment and installed the bug-relevant Python dependencies.
2. Ran bash run_repro.sh with PYTHONPATH pointing at codebase/.
3. Observed that the batch-size-1 and batch-size-2 outputs differ for the same sample.

## Observed behavior

- On this machine, with timm from codebase/ and torch 2.7.0+cu128 on an NVIDIA RTX PRO 6000 Blackwell GPU, the same input sample produces equal outputs within the batch but a different first-row output between batch size 1 and batch size 2. The captured run reports double_rows_equal=True, single_vs_double_equal=False, max_abs_diff=0.0004730224609375, and BUG_REPRODUCED=True.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
