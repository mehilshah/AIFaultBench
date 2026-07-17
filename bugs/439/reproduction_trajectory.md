# Reproduction Trajectory — Bug 439: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/47387](https://github.com/vllm-project/vllm/issues/47387)
- **Repository:** vllm-project/vllm @ `d63c8e944481e057d00dfee20bc49544d291e521`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create an isolated Python 3.12 virtual environment and install the small runtime dependency set from requirements.txt.
2. Force vLLM's pin-memory check to return False, which matches the WSL2 default behavior described in the bug report.
3. Instantiate vllm.v1.worker.gpu.states.RequestState so it constructs StagedWriteTensor(..., uva_instead_of_gpu=True) and raises RuntimeError: UVA is not available.

## Observed behavior

- Running the local harness prints is_uva_available=False and then raises RuntimeError: UVA is not available from vllm/v1/worker/gpu/buffer_utils.py while constructing RequestState, matching the reported failure path. The WSL2-specific pin-memory-off branch was emulated on this host to reach the same code path.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
