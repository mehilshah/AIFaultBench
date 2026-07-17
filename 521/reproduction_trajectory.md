# Reproduction Trajectory — Bug 521: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/46846](https://github.com/huggingface/transformers/issues/46846)
- **Repository:** huggingface/transformers @ `c2fafabbebd83cd6062c809ab602bbeafab639b9`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated venv and installed the repro dependencies plus the local transformers checkout in editable mode.
2. Confirmed the current Qwen3.5 TP plan omits all linear_attn projections.
3. Sharded linear_attn.in_proj_qkv the way a naive colwise TP plan would and ran the block forward pass to trigger the Conv1d channel mismatch.

## Observed behavior

- Qwen3_5TextConfig.base_model_tp_plan still has no linear_attn entries: ['layers.*.linear_attn.in_proj_qkv', 'layers.*.linear_attn.in_proj_z', 'layers.*.linear_attn.in_proj_b', 'layers.*.linear_attn.in_proj_a', 'layers.*.linear_attn.out_proj']
- A tiny Qwen3.5 linear-attention block with a simulated colwise shard of in_proj_qkv fails with RuntimeError: Given groups=12, weight of size [12, 1, 4], expected input[1, 6, 3] to have 12 channels, but got 6 channels instead

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh > repro_stdout.log 2> repro_stderr.log
```
