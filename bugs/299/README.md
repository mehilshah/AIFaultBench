# Bug 299

This folder is the reusable standardized benchmark input for the Transformers / tokenizers build issue reported in https://github.com/huggingface/transformers/issues/47277.

Contents:
- `bug_report.txt`: original issue report
- `codebase/`: local Transformers checkout used for inspection
- `repro.py`: scripted reproduction attempt
- `requirements.txt`: minimal bootstrap requirements for the repro environment
- `setup_env.sh`: creates and activates an isolated virtualenv
- `run_repro.sh`: entrypoint used to run the reproduction
- `manifest.json`: metadata for the bug folder
- `reproduction.json`: machine-readable reproduction outcome
- `repro_stdout.log` and `repro_stderr.log`: saved command output

Reproduction summary:
- issue URL: `https://github.com/huggingface/transformers/issues/47277`
- repository version in this folder: `5.14.0.dev0`
- reported failure: `pthread_cond_clockwait` during `esaxx-rs` build on Termux / Android
- result in this environment: not reproducible here because the host is Linux x86_64 and does not have the Android/Termux `clang++` build stack used in the report
