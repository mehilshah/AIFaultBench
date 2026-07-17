# Bug 148 Repro Bundle

Issue: https://github.com/huggingface/sentence-transformers/issues/3468

## What I ran

The repro uses the exact evaluator path from the report:

```bash
bash run_repro.sh
```

It loads `sentence-transformers/stsb` validation data, moves `sentence-transformers/all-mpnet-base-v2` to CUDA, and evaluates with `EmbeddingSimilarityEvaluator`.

## Outcome

The current checkout does **not** reproduce the reported `TypeError` here.

Observed behavior:

- CUDA is available.
- The 64-example slice completed successfully.
- The full STSB validation split also completed successfully.
- The evaluator returned normal Pearson/Spearman scores instead of failing on `numpy.int64` indexing.

## Files

- `repro.py`: minimal reproducer
- `requirements.txt`: Python dependencies for the repro environment
- `setup_env.sh`: installs the pinned dependencies into the local user site
- `run_repro.sh`: sets up the environment and runs the reproducer
- `reproduction.json`: machine-readable result
- `repro_stdout.log` / `repro_stderr.log`: captured command output
