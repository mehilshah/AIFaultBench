# Bug 086 Reproduction Bundle

This folder reproduces the rotary XPos shape failure reported in `bug_report.txt`
for `x-transformers`.

## What fails

Calling `RotaryEmbedding.forward_from_seq_len()` with `use_xpos=True` reaches
`RotaryEmbedding.forward()`, where the code tries to do
`rearrange(power, 'n -> n 1')` on a 2D tensor. That raises the same
`einops.EinopsError` described in the report.

## Reproduction

1. Install dependencies:
   `bash setup_env.sh`
2. Run the reproducer:
   `bash run_repro.sh`

The run writes:

- `repro_stdout.log`
- `repro_stderr.log`

## Expected result

The reproducer fails with an `einops.EinopsError` showing that the input tensor
shape is 2D when a 1D tensor is expected by `rearrange(power, 'n -> n 1')`.
