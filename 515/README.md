# Bug 515

This folder contains a standalone reproduction of the Hugging Face hub cache
issue reported against `timm`.

Reused inputs:
- `bug_report.txt`
- `codebase/`

Generated artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Repro summary:
- the relevant code path is `codebase/timm/models/_hub.py`
- `load_state_dict_from_hf()` always calls `hf_hub_download()` for the target
  filename, even when the cache file already exists locally
- the repro script fakes the hub downloader so the second call fails like a
  rate limit would
