# Bug 412

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

Reproduction summary:
- The failing op comes from `timm.layers.pos_embed_sincos.apply_rot_embed_cat()`, which calls `tensor_split()`.
- Converting the traced module with Core ML Tools 9.0 raises `NotImplementedError: PyTorch convert function for op 'tensor_split' not implemented.`
- The DINOv3 model path in `timm` uses this helper, so the model export failure in the report is reproducible in this checkout.

Source details:
- issue URL: `https://github.com/huggingface/pytorch-image-models/issues/2594`
- commit hash: `1ec391520aeebe580b0340fcb795cda30d08ef70`
- library: `timm`
- library version: `1.0.20`
