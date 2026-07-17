# Bug 366

This folder contains a standalone repro bundle for the Qwen3-VL
multi-label sequence-classification bug reported in vLLM issue 47956.

What the repro checks:
- a Qwen3-VL config loaded from a checkpoint-style `config.json`
- top-level `num_labels=20` and `problem_type=multi_label_classification`
- the nested Qwen3-VL text config still reports `num_labels=2`

That mismatch is the root of the broken serving path described in the bug
report.

Files:
- `bug_report.txt`: original issue report
- `codebase/`: source snapshot used to inspect the bug
- `repro.py`: executable minimal repro
- `requirements.txt`: runtime deps for the repro
- `setup_env.sh`: bootstrap an isolated environment
- `run_repro.sh`: run the repro in that environment
- `manifest.json`: standardized metadata
- `reproduction.json`: machine-readable result written after running
- `repro_stdout.log` / `repro_stderr.log`: captured command output

Run locally:
```bash
bash run_repro.sh
```
