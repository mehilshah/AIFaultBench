# Bug 436

This folder contains a self-contained reproduction bundle for:
`https://github.com/Lightning-AI/pytorch-lightning/issues/21611`

What is in this folder:
- `bug_report.txt`
- `codebase/` at commit `6805188c711094339e76d81668a4037dd56f7c7a`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Repro summary:
- Lightning source line: `src/lightning/pytorch/plugins/precision/amp.py:116`
- offending behavior: `MixedPrecision.autocast_context_manager()` passes `cache_enabled=False`
- local result: reproducible on the available GPU
