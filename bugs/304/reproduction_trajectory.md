# Reproduction Trajectory — Bug 304: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/48324](https://github.com/vllm-project/vllm/issues/48324)
- **Repository:** vllm-project/vllm @ `4a6440acefbd4d977620bdb6dfb7fb325cd9bda7`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Read bug_report.txt to identify the affected FlashInfer residual quant fusion patterns and the reported mixed-dtype trigger.
2. Inspected codebase/vllm/compilation/passes/fusion/allreduce_rms_fusion.py to compare the residual and non-residual register_replacement calls.
3. Ran bash setup_env.sh and bash run_repro.sh; the script confirmed the missing dtype guard in the residual quant registrations.

## Observed behavior

- Static reproduction succeeded: in codebase/vllm/compilation/passes/fusion/allreduce_rms_fusion.py, AllReduceFusedAddRMSNormStaticQuantFP8Pattern and AllReduceFusedAddRMSNormStaticQuantNVFP4Pattern register without extra_check, while the neighboring non-residual quant patterns register with _rms_input_weight_dtype_match. This matches the bug report's mixed BF16-input / FP32-weight unsafe fusion path.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
