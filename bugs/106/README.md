# Bug 106

This folder contains a self-contained reproduction bundle for:

- issue: `https://github.com/huggingface/pytorch-image-models/issues/2282`
- library: `timm`
- symptom: `Mlp` returns different outputs for batch size 1 vs batch size 2 on identical inputs

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

Validation result:

- reproducible in this environment
- max abs diff between `result_single[0]` and `result_double[0]`: `0.000244140625`
- `result_double[0]` and `result_double[1]` remain equal

Run:

```bash
./run_repro.sh
```
