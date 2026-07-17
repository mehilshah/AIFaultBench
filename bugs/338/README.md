# Bug 338

This folder is the reusable standardized benchmark input for this bug.

Inputs:
- `bug_report.txt`
- `codebase/`

Generated repro bundle:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Repro target:
- issue URL: `https://github.com/huggingface/pytorch-image-models/issues/2616`
- library: `pytorch-image-models`
- library version: `1.0.22`
- model: `tiny_vit_21m_224.dist_in22k_ft_in1k`

The repro uses a synthetic CUDA training loop with `torch.compile(fullgraph=True, backend="inductor")` and a small batch size so it can run within the free VRAM available on this machine.
The environment needs a Blackwell-capable PyTorch build; PyTorch 2.7 is the first stable release line with pre-built CUDA 12.8 wheels for Blackwell support.
