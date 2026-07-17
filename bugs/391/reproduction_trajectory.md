# Reproduction Trajectory — Bug 391: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/13998](https://github.com/huggingface/diffusers/issues/13998)
- **Repository:** huggingface/diffusers @ `7bf00006aa005eae37bcc639fd0f010c183365b4`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a local venv and install the CPU torch/numpy dependencies from requirements.txt.
2. Load codebase/src/diffusers/loaders/lora_conversion_utils.py directly with a stubbed diffusers.utils module.
3. Run the two synthetic kohya FLUX LoRA state dicts from the issue report.

## Observed behavior

- case_a raised KeyError: 'lora_unet_final_layer_adaLN_modulation_1.lora_down.weight'; case_b raised ValueError: 'Incompatible keys detected' with leftover final_layer.alpha keys.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
