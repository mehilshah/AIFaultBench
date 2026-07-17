# Bug 141

This folder reproduces a `safetensors.torch.load(bytes)` failure on a file that contains an empty tensor.

Observed behavior:
- `load_file(path)` succeeds.
- `load(file_bytes)` raises `ValueError: both buffer length (0) and count (-1) must not be 0`.

Run it with:

```bash
bash run_repro.sh
```

Artifacts in this folder:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Source inputs:
- `bug_report.txt`
- `codebase/`
