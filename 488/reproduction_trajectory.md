# Reproduction Trajectory — Bug 488: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/47239](https://github.com/vllm-project/vllm/issues/47239)
- **Repository:** vllm-project/vllm @ `3406e8f83dad17d044d38853f75270c7b636bb95`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Read the GLM-5.2 sparse-indexer logic in `codebase/vllm/models/deepseek_v32/nvidia/attention.py`.
2. Ran `bash setup_env.sh` and then `bash run_repro.sh`.
3. Observed the mismatch between the documented GLM-5.2 carry layers and the current formula output.

## Observed behavior

- codebase/vllm/models/deepseek_v32/nvidia/attention.py:203-215 documents GLM-5.2 index_topk_freq=4 as keeping layers [0,1,2,6,10,...], but the current formula computes a different carry set.
- Running `bash run_repro.sh` exits with status 1 and prints `documented carry layers (from comment): [0, 1, 2, 6, 10]` and `current formula carry layers: [0, 1, 5, 9]`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
