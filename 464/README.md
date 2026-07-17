# Bug 464

This folder contains a minimal reproduction of the Gemma4 unified multimodal dtype bug
reported in `https://github.com/huggingface/transformers/issues/46899`.

What is reproduced:
- `Gemma4UnifiedMultimodalEmbedder.forward()` casts its input tensor to
  `self.embedding_projection.weight.dtype`.
- Under quantized weights, that dtype can be `torch.uint8`.
- The resulting byte tensor causes `masked_scatter` to fail against a `bfloat16`
  destination tensor.

Artifacts:
- `repro.py`: reduced harness that exercises the faulty cast through the source file in `codebase/`
- `requirements.txt`: Python dependencies needed for the repro venv
- `setup_env.sh`: creates `.venv` and installs the pinned runtime
- `run_repro.sh`: executes the repro using the local source tree
- `reproduction.json`: schema-constrained outcome
- `repro_stdout.log`, `repro_stderr.log`: captured repro output

How to run:
- `bash setup_env.sh`
- `bash run_repro.sh`

Notes:
- The bundled repro uses a fake quantized projection with `weight.dtype == torch.uint8`
  to avoid downloading the full Gemma4 checkpoint while still hitting the same buggy path.
- The local source tree is from commit `c96378c4136f5882fee50d8ff8ee1e9588a17eb6`.
