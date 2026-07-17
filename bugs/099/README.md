# Bug 099 Reproduction

This folder reproduces the fp8 failure reported in
`https://github.com/lucidrains/rotary-embedding-torch/issues/24`.

## What fails

`RotaryEmbedding.rotate_queries_or_keys()` calls `get_seq_pos()` with the input tensor dtype.  
When the input tensor is `torch.float8_e4m3fn`, `torch.arange(..., dtype=float8)` is not implemented on CUDA, so the call fails immediately.

## How to run

1. Set up the environment:

```bash
bash setup_env.sh
```

2. Run the repro:

```bash
bash run_repro.sh
```

## Expected result

The fp16 case succeeds.  
The fp8 case raises:

`NotImplementedError: "arange_cuda" not implemented for 'Float8_e4m3fn'`

## Notes

The upstream issue text mentions NaN loss during fp8 training with Transformer Engine.  
In this environment the underlying fp8 path fails earlier and deterministically at the rotary position generation step.
