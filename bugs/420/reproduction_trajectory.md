# Reproduction Trajectory — Bug 420: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/46962](https://github.com/huggingface/transformers/issues/46962)
- **Repository:** huggingface/transformers @ `fdb6d318138c10ad29ac750388917808f50c867c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a tiny `Qwen3Config` with one `full_attention` layer and no sliding window.
2. Patch the causal-mask function to count invocations, then call `create_masks_for_generate`.
3. Pass the returned value into `Qwen3Model.forward` and observe the extra causal-mask call plus the failed dict assertion.

## Observed behavior

- In the local Transformers checkout, `create_masks_for_generate` returned `NoneType` for a Qwen3 config with `layer_types=['full_attention']`. The harness then showed `causal_mask_calls_after_precompute=1` and `causal_mask_calls_after_forward=2`, proving that `Qwen3Model.forward` re-entered `create_causal_mask` instead of consuming a precomputed dict mask.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
