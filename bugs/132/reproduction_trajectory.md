# Reproduction Trajectory — Bug 132: flair

- **Bug report:** [https://github.com/flairNLP/flair/issues/3536](https://github.com/flairNLP/flair/issues/3536)
- **Repository:** flairNLP/flair @ `4d5ede7`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtual environment and installed the repo's Python dependencies.
2. Built a minimal offline harness with `DocumentTFIDFEmbeddings` and `TextPairRegressor`.
3. Called `model._init_model_with_state_dict(model._get_state_dict())` and observed the `document_embeddings` keyword mismatch.

## Observed behavior

- Running `bash run_repro.sh` in the local venv reproduces the reported failure: `TypeError: TextPairRegressor.__init__() got an unexpected keyword argument 'document_embeddings'`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
