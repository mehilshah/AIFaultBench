# Reproduction Trajectory — Bug 138: timm

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2244](https://github.com/huggingface/pytorch-image-models/issues/2244)
- **Repository:** huggingface/pytorch-image-models @ `a6fe31b`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a CUDA-enabled virtual environment and installed the repro dependencies.
2. Loaded timm from the local codebase and instantiated convnext_tiny.fb_in22k with pretrained weights.
3. Ran the model in eval/inference mode on a batch of 4 inputs and on the first sample alone.
4. Compared the first logit and the full first-sample outputs.
5. Observed a nonzero numerical mismatch that matches the reported batch-size dependence.

## Observed behavior

- On this machine, with torch 2.7.0+cu128 and CUDA available, convnext_tiny.fb_in22k in eval mode produced different outputs for the same sample when evaluated inside a batch versus alone. Observed values: batch_out[0][0] = -1.4428796768188477, single_out[0][0] = -1.4428775310516357, abs_diff = 2.1457672119140625e-06, max_abs_diff = 1.6242265701293945e-05, and torch.allclose(batch_out[0], single_out[0]) = False.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
