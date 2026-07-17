# Bug 634

This folder contains the reusable standardized reproduction bundle for
https://github.com/huggingface/transformers/issues/46693.

What is in here:
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

How to run:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

What the harness does:
- Confirms that this snapshot still has the tensor-return regression in
  `codebase/src/transformers/modeling_flash_attention_utils.py`.
- Falls back to a CPU proxy benchmark when CUDA/FlashAttention are unavailable.
- Reports the environment block instead of claiming a full GPU repro.

Relevant upstream fix:
- PR `#47134` "Fix FA performance regression"
- Root cause: `_get_unpad_data()` and `_unpad_input()` should return a Python
  `int` via `.item()` instead of leaving `max_seqlen_in_batch` as a tensor.
