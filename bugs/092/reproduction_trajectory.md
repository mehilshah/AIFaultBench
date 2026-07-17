# Reproduction Trajectory — Bug 092: x-transformers

- **Bug report:** [https://github.com/lucidrains/x-transformers/issues/263](https://github.com/lucidrains/x-transformers/issues/263)
- **Repository:** lucidrains/x-transformers @ `02b0190aa21ceb7688baa4bd40e6a4a3b9880446`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created an isolated virtual environment and installed torch, einops, and packaging.
2. Ran a minimal TransformerWrapper + Decoder(cross_attend=True, attn_flash=True) forward pass with context_mask set to all False.
3. Checked the decoder output for NaNs and finite values.

## Observed behavior

- Running the reported cross-attention setup with an all-false context_mask in the local codebase produced finite decoder outputs; torch.isnan(out).any() was false.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The bug does not reproduce in this checkout: the decoder output is finite under the reported masking condition.
