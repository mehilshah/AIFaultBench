# Bug 273 Reproduction Bundle

This folder contains a self-contained reproduction for the PEFT / Gemma 3 VB-LoRA Dynamo failure reported in:

- https://github.com/huggingface/peft/issues/2627

## What it does

The repro loads `hf-internal-testing/tiny-random-Gemma3ForCausalLM`, wraps it with `VBLoRAConfig`, switches the model to training mode, and calls `generate()` with a static cache and `CompileConfig` so Transformers compiles the generation forward pass.

That path fails with:

- `torch._dynamo.exc.Unsupported: Data-dependent branching`

The traceback points at `codebase/src/peft/tuners/vblora/layer.py` in `_get_lora_matrices()`.

## Files

- `repro.py`: runs the repro and writes `reproduction.json`
- `requirements.txt`: Python dependencies needed for the repro
- `setup_env.sh`: creates a virtual environment and installs dependencies plus the local `codebase`
- `run_repro.sh`: runs the repro and captures `repro_stdout.log` / `repro_stderr.log`
- `manifest.json`: standardized metadata for this bundle

## Usage

1. `bash setup_env.sh`
2. `bash run_repro.sh`

The expected output is a successful reproduction record in `reproduction.json`.
