# Bug 536

Reproduction bundle for vLLM issue 47196:
`[ROCm][gfx942] GPU memory access fault with MTP spec-decode + sparse-MLA decode under cuda graph (GLM-5.1-FP8)`.

## What this bundle does

- Probes the local runtime for the ROCm/AITER prerequisites needed by the report.
- Checks the vulnerable source path in:
  - `codebase/vllm/v1/attention/backends/mla/rocm_aiter_mla_sparse.py`
  - `codebase/vllm/v1/attention/backends/mla/rocm_aiter_mla.py`
- Writes the schema-constrained result to `reproduction.json`.

## Local outcome

This standardized folder is not able to reproduce the GPU crash in the current environment.
The local probe is blocked by:

- broken `torch` import (`libtorch_cuda.so: undefined symbol: ncclCommResume`)
- missing `aiter`
- no ROCm/gfx942 device available in this workspace

## Run

```bash
bash run_repro.sh
```

The command prints the probe summary and updates:

- `repro_stdout.log`
- `repro_stderr.log`
- `reproduction.json`

