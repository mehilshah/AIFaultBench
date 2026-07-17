# Bug 454 Repro

Issue: vLLM / Triton MXFP4 MoE kernels can read poisoned scale memory and produce NaNs on Hopper (`sm90`).

This folder is a local repro bundle for:
`https://github.com/vllm-project/vllm/issues/47303`

Current machine notes:
- GPU is `NVIDIA RTX PRO 6000 Blackwell Max-Q Workstation Edition`
- compute capability is `12.0`, not Hopper `9.0`
- the base `python3` environment also has a broken `torch` import

Because of that, this folder is expected to report a blocker here rather than the Hopper NaN corruption.

## Files
- `repro.py`: environment probe that gates on Hopper and then attempts the kernel repro prerequisites
- `requirements.txt`: minimal runtime dependencies
- `setup_env.sh`: creates a local virtual environment and installs dependencies
- `run_repro.sh`: executes the repro script
- `reproduction.json`: machine-readable outcome

## Run
```bash
bash setup_env.sh
bash run_repro.sh
```

If you are on Hopper with the Triton kernel package available, this is the area to inspect:
- `codebase/vllm/model_executor/layers/fused_moe/experts/gpt_oss_triton_kernels_moe.py`
- issue description in `bug_report.txt`
