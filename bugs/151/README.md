# Bug 151 Reproduction

This bundle reproduces the generation config overwrite described in `bug_report.txt`.

Observed behavior:
- A model-specific default `temperature=1e-6` is attached to `model.generation_config`.
- An explicit `GenerationConfig(temperature=1.0, do_sample=True, max_new_tokens=1)` is passed in.
- `_prepare_generation_config()` rewrites the explicit `temperature=1.0` back to `1e-6`.

Files:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Run:
```bash
bash setup_env.sh
bash run_repro.sh
```
