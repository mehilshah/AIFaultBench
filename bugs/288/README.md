# Bug 288 Reproduction Bundle

This bundle was built from:
- `bug_report.txt`
- `codebase/`

Reported issue:
- `vllm` startup crashes when `torchcodec` is installed with a CUDA wheel that does not match the active PyTorch/CUDA stack.

What this folder currently shows:
- Direct `torchcodec` import fails with `RuntimeError: Could not load libtorchcodec`.
- The checked-in `codebase/vllm/multimodal/video.py` already catches `ImportError` and `RuntimeError` around `from torchcodec.decoders import VideoDecoder`.
- Importing the repo package itself is blocked earlier by an unrelated `torch`/`vLLM` incompatibility in `vllm/env_override.py`.

Files:
- `repro.py` runs the checks and records the failure paths.
- `requirements.txt` lists the minimal Python dependencies used by the repro script.
- `setup_env.sh` installs those dependencies into the current Python environment.
- `run_repro.sh` executes the repro and writes `repro_stdout.log` and `repro_stderr.log`.

Expected outcome in this checkout:
- The exact reported `vllm serve` crash is not reproducible here.
- The closest dependency-level failure is still present in `torchcodec` itself.
