# Bug 377 Reproduction Bundle

This folder reproduces Hugging Face Diffusers issue [#13999](https://github.com/huggingface/diffusers/issues/13999).

Bug summary:
- `_flash_attention_3_varlen_hub` assumes the hub FA3 varlen kernel returns a tuple.
- The reported kernel contract returns a single tensor.
- Python destructuring then consumes tensor rows as if they were tuple elements.

What this bundle does:
- Uses the local `codebase/` source tree.
- Installs a clean CPU-only environment.
- Runs a mock FA3 varlen kernel that returns a tensor, which deterministically triggers the buggy unpacking path on this machine.
- Optionally attempts the real SM90 kernel path when CUDA is available.

Primary entrypoint:
- `run_repro.sh`

Useful files:
- [repro.py](repro.py)
- [requirements.txt](requirements.txt)
- [setup_env.sh](setup_env.sh)
- [run_repro.sh](run_repro.sh)
- [manifest.json](manifest.json)

Expected outcome here:
- The mock repro prints a shape mismatch showing that `_flash_attention_3_varlen_hub` truncated the tensor return.
