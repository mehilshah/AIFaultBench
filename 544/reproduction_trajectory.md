# Reproduction Trajectory — Bug 544: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/13717](https://github.com/huggingface/diffusers/issues/13717)
- **Repository:** huggingface/diffusers @ `6382a3db4dd1e129ce8be68649db6fcbae015e8c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a local venv with Python 3.11 and install torch, diffusers dependencies, and Pillow.
2. Download the reported detailed_notrigger.safetensors checkpoint from Hugging Face into artifacts/.
3. Load a tiny valid LoRA checkpoint through a dummy StableDiffusionXLLoraLoaderMixin subclass.
4. Load the reported checkpoint and observe the ValueError emitted by load_lora_weights().

## Observed behavior

- Running ./run_repro.sh loaded a benign LoRA checkpoint first, then failed on the real checkpoint with ValueError: Invalid LoRA checkpoint. Make sure all LoRA param names contain 'lora' substring.
- The traceback points to codebase/src/diffusers/loaders/lora_pipeline.py line 645.
- The downloaded detailed_notrigger.safetensors file contains 1572 keys, including non-lora keys such as diffusion_model_output_blocks_2_2_conv.alpha and diffusion_model_output_blocks_5_2_conv.alpha.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh > repro_stdout.log 2> repro_stderr.log
```
