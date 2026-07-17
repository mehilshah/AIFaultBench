# Bug 521

This folder contains a self-contained repro for the Qwen3.5 tensor-parallel bug reported in
https://github.com/huggingface/transformers/issues/46846.

What is included:
- `bug_report.txt`
- `codebase/`
- repro artifacts created here:
  - `repro.py`
  - `requirements.txt`
  - `setup_env.sh`
  - `run_repro.sh`
  - `manifest.json`
  - `sitecustomize.py`
  - `reproduction.json`
  - `repro_stdout.log`
  - `repro_stderr.log`

Repro summary:
- The current source still omits `linear_attn.*` from `Qwen3_5TextConfig.base_model_tp_plan`.
- The repro simulates a `colwise` TP shard of `linear_attn.in_proj_qkv`, then calls the
  Qwen3.5 gated-delta block directly.
- The forward pass fails with the same depthwise-conv channel mismatch described in the bug report.

Run the repro:
`bash run_repro.sh`
