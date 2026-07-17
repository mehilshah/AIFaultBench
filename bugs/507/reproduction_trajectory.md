# Reproduction Trajectory — Bug 507: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/48493](https://github.com/vllm-project/vllm/issues/48493)
- **Repository:** vllm-project/vllm @ `b3cfca996c8340263cd1fb770a4c5e0b7f400b26`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Inspect the MiniMax-M3 MoE path in `marlin_moe.py` and verify that `quant_config.gemm1_clamp_limit` is stored and passed into the fused Marlin kernel.
2. Inspect `unquantized_fused_moe_method.py` and verify that `layer.swiglu_limit` is copied into `FusedMoEQuantConfig` as `gemm1_clamp_limit`.
3. Confirm the low-level activation helper still asserts when called without a clamp limit, which is expected and not the reported caller bug.

## Observed behavior

- Low-level activation guard still exists: yes
- Marlin MoE path threads clamp_limit: yes
- Unquantized MoE config plumbs swiglu_limit into gemm1_clamp_limit: yes

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

Current checkout already carries the clamp-limit plumbing for MiniMax-M3 MoE, so the reported Marlin warmup failure is not reproducible here.
