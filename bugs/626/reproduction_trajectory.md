# Reproduction Trajectory — Bug 626: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/46933](https://github.com/vllm-project/vllm/issues/46933)
- **Repository:** vllm-project/vllm @ `9036c89ee410b30913ca8b7d362a7d0805583b51`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Read bug_report.txt and traced the corresponding vLLM code path.
2. Created repro.py, run_repro.sh, setup_env.sh, requirements.txt, Dockerfile, manifest.json, and README.md.
3. Ran bash run_repro.sh; the local machine exposed only one CUDA device, so the repro stopped before starting vLLM.

## Observed behavior

- run_repro.sh records nvidia_smi_gpu_count=1 in repro_stdout.log and exits with the blocker that at least 2 CUDA devices are required.
- The issue report's trigger is TP=2 with OffloadingConnector + CPUOffloadingSpec and CUDA graph capture, which matches the launch command in repro.py and the capture loop in codebase/vllm/v1/worker/gpu_model_runner.py.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

This folder's machine only exposes one CUDA GPU, while the bug report requires tensor_parallel_size=2. The reported hang cannot be exercised without at least two GPUs, so the exact bug is not reproducible here.
