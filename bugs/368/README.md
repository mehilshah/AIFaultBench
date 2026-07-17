# Bug 368

This folder is the reusable standardized benchmark input for this bug.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/`

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Issue context:
- issue URL: `https://github.com/huggingface/pytorch-image-models/issues/2612`
- target library: `huggingface/pytorch-image-models`
- target module: `timm.models.convnext.ConvNeXtBlock`

Result on this host:
- `reproducible`: `false`
- observed full-model timing on supported Torch/CUDA stack: baseline `0.0095s`, patched `0.0100s`
- the reported slowdown is not visible on the available Blackwell + PyTorch 2.9.0+cu128 environment

Run the repro with:
`bash run_repro.sh`
