# Bug 608

This folder contains a self-contained reproduction for the DeepSeek-R1-Distill-Llama-8B tokenizer regression reported in Transformers issue 46710.

What the repro checks:
- `transformers==5.9.0`
- `AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Llama-8B")`
- round-tripping ordinary English through `tokenizer.encode(...)` and `tokenizer.decode(...)`

Observed failure:
- the decoded text drops spaces, e.g. `What is 1+1? Answer briefly.` becomes `Whatis1+1?Answerbriefly.`
- the same model tokenizer also round-trips the chat prompt without preserving spacing

Files:
- `bug_report.txt`
- `codebase/`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Run:
`bash run_repro.sh`

Source summary:
- issue URL: `https://github.com/huggingface/transformers/issues/46710`
- commit hash: `b4b5244c9c7cdb80d0aaafdb8f35244612788532`
- library: `transformers`
- library version used for repro: `5.9.0`
