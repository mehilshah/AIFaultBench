# Bug 033

This folder is a self-contained reproduction bundle for:
`https://github.com/NVIDIA/DeepLearningExamples/issues/1250`

What is included:
- `bug_report.txt` from the benchmark input
- `codebase/` from the standardized source snapshot
- Reproduction artifacts:
  - `repro.py`
  - `requirements.txt`
  - `setup_env.sh`
  - `run_repro.sh`
  - `manifest.json`
  - `reproduction.json`
  - `repro_stdout.log`
  - `repro_stderr.log`

Reproduction summary:
- The reported failure is a `torch.matmul` shape mismatch in `ConvSE3`'s self-interaction path.
- A minimal harness that mirrors that branch reproduces the exact error:
  `Expected size for first two dimensions of batch2 tensor to be: [8910, 1] but got: [8910, 3].`

Run locally:
`bash run_repro.sh`
