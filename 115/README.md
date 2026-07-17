# Bug 115

This folder is a self-contained reproduction bundle for axolotl issue 3079.

What it shows:
- sweep permutations are generated from the base config
- each generated config keeps the same `output_dir`
- that makes later sweep runs overwrite earlier ones

Files:
- `bug_report.txt`: source issue report
- `codebase/`: local source snapshot used to reproduce the bug
- `base_config.yml`: minimal base config with a fixed `output_dir`
- `sweep.yml`: sweep parameters that generate multiple permutations
- `repro.py`: runs the local sweep generation path and prints evidence
- `run_repro.sh`: convenience wrapper for the repro
- `setup_env.sh`: optional local environment bootstrap
- `requirements.txt`: minimal dependency list for the repro script
- `manifest.json`: bundle metadata

Run:
```bash
bash run_repro.sh
```
