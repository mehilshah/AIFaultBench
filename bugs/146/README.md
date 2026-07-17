# Bug 146

This folder is the reusable standardized benchmark input for this bug.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/` when available

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction summary:
- The local `sentence_transformers.models.Transformer.tokenize()` strips leading and trailing whitespace before tokenization.
- `SentenceTransformer.encode()` therefore collapses `" test"` and `"test"` to the same tokenization path even when the underlying tokenizer distinguishes them.
- The repro script uses a small GPT-2 model to keep the bundle lightweight while still exercising whitespace-sensitive tokenization.

Source summary:
- issue URL: `https://github.com/huggingface/sentence-transformers/issues/3262`
- commit hash: `not found in Dataset.csv`
- inferred library: `sentence-transformers`
- inferred library version: `3.5.0.dev0`
- bug report source: `bug_report.txt`
- codebase source: `codebase`
