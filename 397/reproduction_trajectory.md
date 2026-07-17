# Reproduction Trajectory — Bug 397: pytorch-image-models

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2600](https://github.com/huggingface/pytorch-image-models/issues/2600)
- **Repository:** huggingface/pytorch-image-models @ `cebc007d66041fee4e468305065872ec1200bec2`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a clean CPU-only Python environment with torch 2.7.1 and torchvision 0.22.1.
2. Ran the local ViT training harness twice with the same seed (42).
3. Ran the same harness once with a different seed (43) as a control.
4. Compared the captured outputs and model hashes.

## Observed behavior

- Two consecutive seed-42 runs produced identical epoch losses, predictions, and model SHA256 hashes; a seed-43 control run produced different losses and a different hash.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported nondeterminism did not appear here. Same-seed ViT runs were exactly reproducible in this environment, so the issue could not be reproduced from the provided inputs.
