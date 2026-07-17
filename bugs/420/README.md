# Bug 420

This folder contains a self-contained reproduction bundle for the Qwen3 mask regression described in `bug_report.txt`.

Inputs:
- `bug_report.txt`
- `codebase/` at commit `fdb6d318138c10ad29ac750388917808f50c867c`

Generated artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Repro summary:
- `create_masks_for_generate` returns a bare mask for `layer_types=['full_attention']`
- `Qwen3Model.forward` treats that value as not-yet-prepared and calls `create_causal_mask` again
- the tiny harness records two causal-mask calls instead of one

Run locally:
`bash setup_env.sh && bash run_repro.sh`

Source summary:
- issue URL: `https://github.com/huggingface/transformers/issues/46962`
- commit hash: `fdb6d318138c10ad29ac750388917808f50c867c`
- library: `transformers`
- library version: `5.13.0.dev0`
