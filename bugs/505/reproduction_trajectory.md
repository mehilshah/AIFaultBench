# Reproduction Trajectory — Bug 505: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/48831](https://github.com/vllm-project/vllm/issues/48831)
- **Repository:** vllm-project/vllm @ `dc9f845ddc54c1df38fdbce5afe03f9fd15813bd`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a clean virtualenv and installed torch==2.11.0+cu130 plus numpy from the CUDA wheel index.
2. Ran repro.py, which enqueued an async H2D copy on one CUDA stream and immediately read the destination on another stream without synchronization.
3. Confirmed the consumer observed stale data before synchronization and the expected value after torch.cuda.synchronize().

## Observed behavior

- The repro on CUDA 13.0.2 with torch 2.11.0+cu130 observed stale data on the unsynchronized read: async_read_value=0 and async_read_score=0.00004540, while the synchronized follow-up saw sync_read_value=100 and sync_read_score=0.99995458.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
