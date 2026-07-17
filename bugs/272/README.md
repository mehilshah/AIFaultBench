# Bug 272

This bundle validates the EAGLE speculative-decoding `lm_head` lookup path for multimodal wrapper models.

Status in this snapshot:
- `vllm/v1/worker/gpu/spec_decode/eagle/utils.py` already resolves `lm_head` through `get_target_lm_head()`
- the vulnerable `getattr(target_model, "lm_head", None)` pattern from the report is not the active code path
- the original crash is therefore not reproducible in this checked-in tree

Run:
```bash
bash run_repro.sh
```

Outputs:
- `repro_stdout.log`
- `repro_stderr.log`
- `reproduction.json`

Relevant source locations:
- [`codebase/vllm/v1/worker/gpu/spec_decode/eagle/utils.py`](codebase/vllm/v1/worker/gpu/spec_decode/eagle/utils.py#L28)
- [`codebase/vllm/v1/spec_decode/llm_base_proposer.py`](codebase/vllm/v1/spec_decode/llm_base_proposer.py#L1501)
