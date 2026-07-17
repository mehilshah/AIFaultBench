# Reproduction Trajectory — Bug 157: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/43159](https://github.com/huggingface/transformers/issues/43159)
- **Repository:** huggingface/transformers @ `3aa2154`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a venv with system site packages and installed the hub dependency needed for the local transformers checkout to import cleanly.
2. Ran the exact OPT-125m safetensors load path from the bug report against codebase/src.
3. Inspected lm_head.weight and model.decoder.embed_tokens.weight after loading; both were materialized on cpu and shared storage.

## Observed behavior

- With local codebase/src and a clean venv overlaying huggingface_hub==1.2.2, AutoModelForCausalLM.from_pretrained('facebook/opt-125m', torch_dtype=torch.float16, use_safetensors=True) completed successfully. The loaded tensors were on cpu, not meta: lm_head.weight.is_meta=false and model.decoder.embed_tokens.weight.is_meta=false, and the two weights shared storage.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
