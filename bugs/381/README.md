# Bug 381

Issue: `https://github.com/vllm-project/vllm/issues/47935`

Verdict for this folder: not reproducible here.

Why:
- The local runtime cannot import the installed `torch` wheel because `libtorch_cuda.so` fails to resolve `ncclCommResume`.
- The reported path is CUDA-only FlashMLA / DeepSeek-V4 sparse MLA logic, so a working CUDA build plus Hopper/Blackwell-capable FlashMLA support is required.
- The current source tree already contains the C128A top-k padding fix in `vllm/models/deepseek_v4/sparse_mla.py`, so the exact assertion described in the bug report is not present in this snapshot.

Artifacts in this folder:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction command:
`bash run_repro.sh`
