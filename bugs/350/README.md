# Bug 350

This folder is a self-contained repro bundle for the DeepSpeed `torch.func`
compatibility bug described in `bug_report.txt`.

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

Repro summary:
- issue URL: `https://github.com/deepspeedai/DeepSpeed/issues/7913`
- library: `DeepSpeed`
- library version: `0.18.8`
- codebase source: local `codebase/`
- bug trigger: `LinearFunctionForZeroStage3` lacks `setup_context`, so
  `torch.func.grad_and_value` raises the functorch autograd.Function error.

Run:
`bash run_repro.sh`
