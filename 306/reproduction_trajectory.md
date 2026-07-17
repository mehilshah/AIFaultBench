# Reproduction Trajectory — Bug 306: pytorch-image-models

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2682](https://github.com/huggingface/pytorch-image-models/issues/2682)
- **Repository:** huggingface/pytorch-image-models @ `a94c10fce182362e26e128e1b51863dff2a1d558`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create an isolated virtualenv and install the bundle requirements.
2. Run repro.py, which compares two pretrained resnet50_clip.openai feature-extraction instantiations.
3. Compare the same model after reset_classifier(0, '') as the documented workaround.

## Observed behavior

- buggy_diff=0.7813611030578613; workaround_diff=0.0; buggy_proj_type=Linear; workaround_proj_type=Identity

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
