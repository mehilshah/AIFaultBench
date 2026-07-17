# Bug 284

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

Repro target:
- issue URL: `https://github.com/huggingface/diffusers/issues/14146`
- commit hash: `208704a27a6f362b67cd1a04fa1db0b98036d26f`
- library: `diffusers`
- suspected trigger: `Krea2Pipeline` on ROCm/gfx1201 with `torch.bfloat16`, sequential CPU offload, and `transformer.compile()`

Run the repro:
`bash run_repro.sh`

Expected behavior on matching hardware:
- load `krea/Krea-2-Turbo`
- run the exact prompt from the report
- save `krea2.png`

Local environment note:
- this workspace does not expose a ROCm/CUDA accelerator, so the script is expected to stop with a blocking reason instead of producing the image corruption reported upstream.
- the repro uses the checked-in `codebase/` via `PYTHONPATH`; install a ROCm-enabled PyTorch build separately on the target machine if it is not already present.
