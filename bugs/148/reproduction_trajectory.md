# Reproduction Trajectory — Bug 148: sentence-transformers

- **Bug report:** [https://github.com/huggingface/sentence-transformers/issues/3468](https://github.com/huggingface/sentence-transformers/issues/3468)
- **Repository:** huggingface/sentence-transformers @ `5eb2a1b`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Installed the reported-era dependency set into the local user site.
2. Ran the issue's evaluation flow against sentence-transformers/all-mpnet-base-v2 on CUDA using the local codebase.
3. Confirmed the full sentence-transformers/stsb validation split completes successfully.

## Observed behavior

- On the local checkout with CUDA available, the exact STSB EmbeddingSimilarityEvaluator path completed successfully on the full validation split. The run printed pearson_cosine=0.8806072235811941 and spearman_cosine=0.8810194487011652 instead of raising the reported TypeError.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The bug is not reproducible in this folder: the current checkout's encode/evaluator path executes successfully on CUDA, so there is no failing traceback to capture.
