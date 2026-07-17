# Reproduction Trajectory — Bug 588: pytorch-image-models

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2453](https://github.com/huggingface/pytorch-image-models/issues/2453)
- **Repository:** huggingface/pytorch-image-models @ `e44f14d7d2f557b9f3add82ee4f1ed2beefbb30d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a clean local virtualenv and installed the repro dependencies.
2. Ran repro.py through run_repro.sh.
3. Observed the TypeError on the bad pretrained_cfg_overlay value.
4. Verified the backbone extraction path works with a valid overlay mapping.

## Observed behavior

- Running the report-shaped call to timm.create_model('mobilenetv4_conv_medium', pretrained=True, pretrained_cfg_overlay='file=./pytorch_model.bin') raised TypeError: dataclasses.replace() argument after ** must be a mapping, not str.
- A control call with pretrained_cfg_overlay={'file': './pytorch_model.bin'} succeeded, and a backbone built from model.conv_stem, model.bn1, and model.blocks[:3] produced output shape (1, 160, 14, 14).

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
