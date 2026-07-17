# Bug 498

Reproduction bundle for:
`https://github.com/huggingface/diffusers/issues/13819`

Files in this folder:
- `bug_report.txt`
- `codebase/`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Run:
`bash setup_env.sh && bash run_repro.sh`

The repro script runs the docs snippet for `QwenImageEditPipeline`, saves the output image,
and records simple pixel statistics so a black image is explicit in the logs and result JSON.

