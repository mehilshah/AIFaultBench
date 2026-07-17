# Bug 507 Repro Bundle

This folder captures a standalone reproduction attempt for vLLM issue
`#48493`:
`SWIGLUOAI_UNINTERLEAVE requires clamp_limit` blocks MiniMax-M3 AWQ/GPTQ INT4.

## Result

The current `codebase/` already contains the clamp-limit plumbing that the
report says was missing:

- `vllm/model_executor/layers/fused_moe/experts/marlin_moe.py` stores
  `quant_config.gemm1_clamp_limit` and passes it into `fused_marlin_moe()`.
- `vllm/model_executor/layers/fused_moe/unquantized_fused_moe_method.py`
  forwards `layer.swiglu_limit` into `FusedMoEQuantConfig`.
- `vllm/model_executor/layers/fused_moe/activation.py` still asserts that
  `SWIGLUOAI_UNINTERLEAVE` needs a clamp limit, which is expected behavior for
  the low-level activation helper.

Because the caller path is already wired up in this checkout, the bug is not
reproducible here.

## Run

```bash
bash run_repro.sh
```

The command writes:

- `repro_stdout.log`
- `repro_stderr.log`
- `reproduction.json`
