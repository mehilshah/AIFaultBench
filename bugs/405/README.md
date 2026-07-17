# Bug 405

This folder is the reusable standardized benchmark input for this bug.

Inputs:
- `bug_report.txt`
- `codebase/` at `huggingface/transformers@181beb3ba4c47098ed8cbc97ee250d1d45ae0107`

Generated reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Run the repro with:
`bash run_repro.sh`

Observed behavior:
- `AutoProcessor.from_pretrained("facebook/dinov3-vits16-pretrain-lvd1689m")` against a local `HF_ENDPOINT` that returns `429` for file downloads retries each probe multiple times.
- The request log shows repeated HEAD requests for `processor_config.json`, `preprocessor_config.json`, `video_preprocessor_config.json`, `tokenizer_config.json`, and `config.json`.

Source summary:
- issue URL: `https://github.com/huggingface/transformers/issues/46981`
- commit hash: `181beb3ba4c47098ed8cbc97ee250d1d45ae0107`
- library: `transformers`
- library version: `5.13.0.dev0`
- bug report source: `bug_report.txt`
