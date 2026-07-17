# Reproduction Trajectory — Bug 536: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/47196](https://github.com/vllm-project/vllm/issues/47196)
- **Repository:** vllm-project/vllm @ `248d1fbb711b210784ab880593403d665a4731bd`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Inspect the ROCm sparse-MLA builder in codebase/vllm/v1/attention/backends/mla/rocm_aiter_mla_sparse.py.
2. Inspect the dense MLA builder in codebase/vllm/v1/attention/backends/mla/rocm_aiter_mla.py.
3. Attempt to import the local runtime dependencies and probe for ROCm/GPU support.
4. Record the result in reproduction.json.

## Observed behavior

- Sparse MLA build() recomputes shared work buffers via get_mla_metadata_v1() at codebase/vllm/v1/attention/backends/mla/rocm_aiter_mla_sparse.py:542-560.
- Dense MLA build() also recomputes persistent decode metadata via get_mla_metadata_v1() at codebase/vllm/v1/attention/backends/mla/rocm_aiter_mla.py:523-543.
- Neither MLA build() path inserts a stream sync after the metadata write before returning the tensors to the captured decode path.
- torch import failed: /users/grad/mehil/.local/lib/python3.12/site-packages/torch/lib/libtorch_cuda.so: undefined symbol: ncclCommResume
- aiter is not installed
- no ROCm runtime utilities found

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

torch import failed: /users/grad/mehil/.local/lib/python3.12/site-packages/torch/lib/libtorch_cuda.so: undefined symbol: ncclCommResume; aiter is not installed; no ROCm runtime utilities found
