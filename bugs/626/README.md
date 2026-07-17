# Bug 626 Repro Bundle

This folder reproduces vLLM issue [#46933](https://github.com/vllm-project/vllm/issues/46933):
`TP + CPU KV Offloading + CUDA Graph capture hangs`.

## Contents

- `bug_report.txt`: upstream issue report
- `codebase/`: local source snapshot used for the repro
- `repro.py`: reproducer entry point
- `run_repro.sh`: wrapper that records stdout/stderr logs
- `setup_env.sh`: environment bootstrap helper
- `requirements.txt`: inferred Python dependencies
- `manifest.json`: folder metadata
- `reproduction.json`: structured result produced from the local run
- `repro_stdout.log`, `repro_stderr.log`: captured command output

## Local result

This machine exposes only one CUDA device, while the reported bug requires
`tensor_parallel_size=2` and therefore at least two GPUs. The local run stops
before launching vLLM and records that blocker.

## Reproduction command

```bash
bash run_repro.sh
```

## Expected command on capable hardware

The reproducer uses the same serving flags from the bug report:

```bash
python3 -m vllm.entrypoints.cli.main serve openai/gpt-oss-120b \
  --tensor-parallel-size=2 \
  --kv-transfer-config '{"kv_connector":"OffloadingConnector","kv_role":"kv_both","kv_connector_extra_config":{"spec_name":"CPUOffloadingSpec","cpu_bytes_to_use":26843545600,"eviction_policy":"lru"}}' \
  --enable-prefix-caching \
  --no-disable-hybrid-kv-cache-manager
```

