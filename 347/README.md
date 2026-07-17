# Bug 347

This folder is the reusable standardized benchmark input for this bug.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/`

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Issue summary:
- issue URL: `https://github.com/huggingface/diffusers/issues/14063`
- title: `Kandinsky5 pipeline does not support device_map=balanced`
- relevant source: `codebase/src/diffusers/pipelines/kandinsky5/pipeline_kandinsky_i2i.py`
- buggy concat site: `torch.cat([latents, image_latents, torch.ones_like(latents[..., :1])], -1)`

Reproduction notes:
- The harness uses CPU `torch` and a meta-device tensor to simulate the reported balanced device-map split.
- That reproduces the same failure mode: the VAE-side image latents and the generated noise latents are not on the same device when concatenated.

Typical flow:
1. `bash setup_env.sh`
2. `bash run_repro.sh`
3. Inspect `repro_stdout.log` and `repro_stderr.log`
