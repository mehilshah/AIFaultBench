# Reproduction Trajectory — Bug 450: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/13920](https://github.com/huggingface/diffusers/issues/13920)
- **Repository:** huggingface/diffusers @ `784fa62652fb2719d415830f918fc32a49ecc7a1`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a minimal local codebase tree containing the bug-relevant diffusers rotary-embedding module.
2. Created an isolated Python 3.11 virtual environment and installed the minimal runtime dependencies.
3. Ran repro.py against diffusers.models.transformers.transformer_ideogram4.Ideogram4MRoPE.
4. Observed that torch.autocast(..., dtype=torch.bfloat16) makes the reported image positions share identical rotary embeddings.

## Observed behavior

- On torch 2.7.1+cu126, the non-autocast path preserved distinct image positions while CPU autocast collapsed them: ref_equal_01=false, ref_equal_02=false, ac_equal_01=true, ac_equal_02=true, max_diff=1.9335092306137085.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
