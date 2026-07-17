# Reproduction Trajectory — Bug 627: pytorch-image-models

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2407](https://github.com/huggingface/pytorch-image-models/issues/2407)
- **Repository:** huggingface/pytorch-image-models @ `ef7dec8e434d1279071b865187ebb7304922e846`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Create an isolated CPU Python environment with torch and torchvision installed.
2. Run the local repro bundle via bash run_repro.sh.
3. Inspect stdout and stderr to confirm the checkpoint saver completed normally.

## Observed behavior

- A local CheckpointSaver probe completed 5 epochs in a clean CPU venv, rotating checkpoint-0 through checkpoint-4 without raising FileNotFoundError. The captured stdout shows completed_without_error=true and an empty stderr log.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported missing tmp.pth.tar rename did not occur on this local filesystem, so the issue is not reproducible here without the original Hugging Face Spaces / multi-GPU setup.
