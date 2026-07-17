# Reproduction Trajectory — Bug 137: evaluate

- **Bug report:** [https://github.com/huggingface/evaluate/issues/564](https://github.com/huggingface/evaluate/issues/564)
- **Repository:** huggingface/evaluate @ `8dfe057`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Install the local evaluate package from codebase/ together with rouge_score, absl-py, and nltk.
2. Load the local rouge metric from codebase/metrics/rouge.
3. Compute scores for identical Nepali prediction/reference strings with the default tokenizer.
4. Observe all ROUGE scores are 0.0, then rerun with tokenizer=str.split and observe all scores become 1.0.

## Observed behavior

- Running evaluate.load on the local rouge metric with identical Nepali prediction/reference strings returns rouge1/rouge2/rougeL/rougeLsum of 0.0 by default, while passing tokenizer=str.split returns 1.0 for the same inputs.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
