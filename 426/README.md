# Bug 426

Repro bundle for `https://github.com/huggingface/peft/issues/499`.

What this bundle does:
- Creates a local venv with a CUDA-capable PyTorch wheel that supports this Blackwell GPU.
- Installs the pinned PEFT checkout from `codebase/`.
- Runs a tiny Bloom sequence-classification model through `PromptEncoder` with FSDP CPU offload.
- Triggers a device-mismatch failure inside `peft_model.py` during prompt-tuning forward.

Files:
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

Reproduction:
- `bash setup_env.sh`
- `bash run_repro.sh`

Observed failure:
- `RuntimeError: Expected all tensors to be on the same device`
- Stack trace reaches `codebase/src/peft/peft_model.py` in the prompt-tuning forward path.

Pinned sources:
- issue URL: `https://github.com/huggingface/peft/issues/499`
- commit hash: `3714aa2fff158fdfa637b2b65952580801d890b2`
