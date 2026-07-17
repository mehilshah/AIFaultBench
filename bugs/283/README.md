# Bug 283

This folder is a self-contained reproduction bundle for
[`huggingface/transformers#47332`](https://github.com/huggingface/transformers/issues/47332).

Outcome in this checkout:
- The reported `save_pretrained` failure is not reproducible.
- A mixed CPU/disk offload load succeeds, and `save_pretrained()` writes `model.safetensors` successfully.

Included artifacts:
- `bug_report.txt`
- `codebase/`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Suggested local run:
```bash
./setup_env.sh
./run_repro.sh
```

The reproducer uses the local source tree via `PYTHONPATH=codebase/src` and a tiny
`Qwen3VLForConditionalGeneration` checkpoint to exercise the offload/save path without
downloading the full upstream model.
