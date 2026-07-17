# Bug 043

Reproduction bundle for fairseq issue `#5130`.

Bug summary:
- `examples/mms/tts/infer.py` imports `commons` at top level.
- The repo does not ship that module.
- Running the script in a minimal environment produces `ModuleNotFoundError: No module named 'commons'`.

Files in this folder:
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

Repro approach:
- Create temporary stub modules for unrelated imports (`torch`, `numpy`) so the script can start.
- Run `codebase/examples/mms/tts/infer.py` from `codebase/examples/mms/tts`.
- Confirm the failure occurs on `import commons`.

Entry point:
- `bash run_repro.sh`
