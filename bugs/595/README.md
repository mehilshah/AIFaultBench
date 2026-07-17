# Bug 595

Reproduction bundle for the `transformers` issue where `AutoProcessor.from_pretrained("HuggingFaceTB/SmolVLM-256M-Instruct")` raises a misleading `ValueError: Unrecognized image processor...` when `torchvision` is unavailable.

Included inputs:
- `bug_report.txt`
- `codebase/`

Generated reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Primary reproduction:
- `bash setup_env.sh`
- `bash run_repro.sh`

Observed result:
- `AutoProcessor.from_pretrained("HuggingFaceTB/SmolVLM-256M-Instruct")` fails with `ValueError: Unrecognized image processor in HuggingFaceTB/SmolVLM-256M-Instruct...`
- This happens after `torchvision` is blocked, matching the bug report.

References:
- Issue URL: `https://github.com/huggingface/transformers/issues/46726`
- Local codebase snapshot: `transformers` `5.13.0.dev0` from `codebase/`
