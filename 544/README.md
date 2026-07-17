# Bug 544

Standardized repro bundle for the diffusers LoRA checkpoint validation issue.

Inputs:
- `bug_report.txt`
- `codebase/`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Repro summary:
- issue URL: `https://github.com/huggingface/diffusers/issues/13717`
- library: `diffusers`
- local codebase version: `0.39.0.dev0`
- trigger: `load_lora_weights()` rejects a real checkpoint whose keys include non-`lora` names such as `diffusion_model_output_blocks_2_2_conv.alpha`

Run:
`bash run_repro.sh`
