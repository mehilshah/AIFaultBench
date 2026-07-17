# Bug 268

This folder is a standalone reproduction bundle for the diffusers offline-mode
LoRA weight-name regression described in `bug_report.txt`.

What is included:
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

Reproduction summary:
- `HF_HUB_OFFLINE=1` and `local_files_only=True` both reject an explicit local
  temporary directory containing `adapter.safetensors`.
- The failure is `ValueError: When using the offline mode, you must specify a
  weight_name.`
- The failing path is `_best_guess_weight_name()` in
  `codebase/src/diffusers/loaders/lora_base.py`.

Run:
```bash
bash run_repro.sh
```
