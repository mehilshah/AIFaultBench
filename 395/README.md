# Bug 395

This folder contains a minimal repro bundle for:

- Issue: `https://github.com/vllm-project/vllm/issues/47836`
- Commit snapshot: `b4cfbc24d33ca17bc764a75ffe749654654521c1`

The bug report points to `vllm/model_executor/layers/fused_moe/routed_experts.py`
and the failing access:

```python
expert_data = param.data if full_load else param.data[expert_id]
```

The local repro script triggers that exact branch with a zero-sized expert
tensor and `expert_id = 0`, reproducing the `IndexError` without requiring a
full model download.

Files generated for reproduction:

- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`
