# Reproduction Trajectory — Bug 609: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/13484](https://github.com/huggingface/diffusers/issues/13484)
- **Repository:** huggingface/diffusers @ `71a6fd9f0df04d3764dfa999268a05d87903a85a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a clean virtual environment with CPU PyTorch and the small repro dependency set.
2. Run `bash run_repro.sh` to execute the synthetic Flux2 non-diffusers LoRA conversion path.
3. Observe that the converter fails with the same leftover `guidance_in.*` keys reported in the issue.

## Observed behavior

- Running the minimal Flux2 AI-toolkit LoRA repro in `repro.py` raises `ValueError: `original_state_dict` should be empty at this point but has original_state_dict.keys()=dict_keys(['guidance_in.in_layer.lora_A.weight', 'guidance_in.out_layer.lora_A.weight', 'guidance_in.in_layer.lora_B.weight', 'guidance_in.out_layer.lora_B.weight'])` from `diffusers/loaders/lora_conversion_utils.py:2438`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
