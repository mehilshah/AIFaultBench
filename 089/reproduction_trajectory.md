# Reproduction Trajectory — Bug 089: x-transformers

- **Bug report:** [https://github.com/lucidrains/x-transformers/issues/282](https://github.com/lucidrains/x-transformers/issues/282)
- **Repository:** lucidrains/x-transformers @ `eeed50391855f8d552edc866701952f38015e415`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a minimal Decoder configuration using the current attn_* API surface.
2. Installed torch, einops, packaging, and numpy into an isolated venv.
3. Ran a forward pass on a 1-layer TransformerWrapper with heads=4 and attn_kv_heads=2.
4. Observed the tensor shape mismatch when qk_norm_dim_scale multiplies k by a scale tensor sized for heads instead of kv_heads.

## Observed behavior

- Running a minimal TransformerWrapper with attn_kv_heads=2, attn_qk_norm=True, and attn_qk_norm_dim_scale=True raises RuntimeError at codebase/x_transformers/x_transformers.py:1172: 'The size of tensor a (2) must match the size of tensor b (4) at non-singleton dimension 1'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
