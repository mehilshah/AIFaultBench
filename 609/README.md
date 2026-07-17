# Bug 609 Reproduction

This folder reproduces the Flux2 LoRA loading failure reported in:
`https://github.com/huggingface/diffusers/issues/13484`

The failure happens in `Flux2LoraLoaderMixin` when a non-diffusers Flux2 LoRA
checkpoint reaches `_convert_non_diffusers_flux2_lora_to_diffusers()` with
`guidance_in.*` keys present. Those keys are left over after conversion and the
helper raises:

`ValueError: \`original_state_dict\` should be empty at this point ...`

Files:
- `repro.py`: minimal synthetic reproducer
- `requirements.txt`: runtime dependencies for the repro
- `setup_env.sh`: creates an isolated venv and installs dependencies
- `run_repro.sh`: executes the repro and captures logs
- `repro_stdout.log` / `repro_stderr.log`: output from the last run
- `reproduction.json`: schema-constrained result summary

Run:
```bash
bash run_repro.sh
```
