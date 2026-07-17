# Reproduction Trajectory — Bug 561: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/47054](https://github.com/vllm-project/vllm/issues/47054)
- **Repository:** vllm-project/vllm @ `7be582697b27277e2756a3878f563fa9dfea30aa`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Inspect the source-tree packing logic in vllm/v1/core/kv_cache_utils.py.
2. Compute the cross-layer packed KV cache layout for the reported HMA group structure.
3. Compare the resulting block stride against the single-layer page size.

## Observed behavior

- Source-derived packed layout uses block_stride=16384 bytes for a page size of 8192 bytes.
- That is exactly the 2x-page stride mismatch described in the issue report.
- Local CUDA device: NVIDIA RTX PRO 6000 Blackwell Max-Q Workstation Edition (12.0), which is not the reported H100 Hopper setup.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
MODEL="openai/gpt-oss-120b"
TP_SIZE=2
CPU_BYTES=26843545600

KV_TRANSFER_CONFIG=$(cat <<EOF
{
  "kv_connector": "OffloadingConnector",
  "kv_role": "kv_both",
  "kv_connector_extra_config": {
    "enable_cross_layers_blocks": "True",
    "spec_name": "CPUOffloadingSpec",
    "cpu_bytes_to_use": ${CPU_BYTES},
    "eviction_policy": "lru"
  }
}
EOF
)

vllm serve "${MODEL}"       --tensor-parallel-size="${TP_SIZE}"       --kv-transfer-config "${KV_TRANSFER_CONFIG}"       --enable-prefix-caching       --no-disable-hybrid-kv-cache-manager

lm_eval   --model local-completions   --model_args "base_url=http://127.0.0.1:8000/v1/completions,model=${MODEL},tokenized_requests=False,num_concurrent=1000,trust_remote_code=True"   --tasks gsm8k   --seed 42   --num_fewshot 5   --gen_kwargs temperature=0.0
```

## Why it does not reproduce on the reference machine

The exact issue report is not reproduced here: the local GPU is NVIDIA RTX PRO 6000 Blackwell Max-Q Workstation Edition, not the Hopper H100 reported in the bug, and the full vllm serve + lm_eval workload was not executed.
