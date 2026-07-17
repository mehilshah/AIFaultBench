# Bug 425

This folder is the reusable standardized benchmark input for this bug.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/`

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction summary:
- The failing branch is `DSparkSpeculator.load_draft_model()` in
  `codebase/vllm/v1/worker/gpu/spec_decode/dspark/speculator.py`.
- The corresponding DeepSeek-V4 DSpark model wrapper in
  `codebase/vllm/models/deepseek_v4/nvidia/dspark.py` does not define
  `draft_id_to_target_id`.
- The repro script triggers the same attribute access with a model stub named
  `DSparkDeepseekV4ForCausalLM`, which raises the same `AttributeError`.

Source summary:
- issue URL: `https://github.com/vllm-project/vllm/issues/47418`
- commit hash: `25fcb65d51deef0026aa34e6067703da4a91f956`
- inferred library: `vllm`
- inferred library version: `unknown`
- bug report source: `bug_report.txt`
- codebase source: `vllm-project/vllm@25fcb65d51deef0026aa34e6067703da4a91f956`
