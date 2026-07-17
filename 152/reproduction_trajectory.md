# Reproduction Trajectory — Bug 152: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/42794](https://github.com/huggingface/transformers/issues/42794)
- **Repository:** huggingface/transformers @ `8ebfd84`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a local virtualenv and install the repo runtime dependencies from `requirements.txt`.
2. Run `repro.py` with `PYTHONPATH=codebase/src` so the local transformers checkout is used.
3. Load `naver-clova-ix/donut-base-finetuned-docvqa` through `pipeline('document-question-answering', ...)` and call it with the invoice image URL and question from the report.

## Observed behavior

- Running the report's donut document-question-answering pipeline on this checkout loads successfully, then fails in `codebase/src/transformers/generation/utils.py:2145` with `ValueError: `decoder_start_token_id` or `bos_token_id` has to be defined for encoder-decoder generation.`
- The model config printed by the repro has `decoder_start_token_id=None` and `bos_token_id=None` before generation.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
