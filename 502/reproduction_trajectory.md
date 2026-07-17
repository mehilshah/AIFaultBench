# Reproduction Trajectory — Bug 502: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/47215](https://github.com/vllm-project/vllm/issues/47215)
- **Repository:** vllm-project/vllm @ `28242824e00856cf4f3d3f45c959ab1e6501a91b`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. bash setup_env.sh
2. bash run_repro.sh

## Observed behavior

- `codebase/vllm/model_executor/layers/quantization/modelopt.py` already contains a dedicated `W4A16_NVFP4` branch in `ModelOptMixedPrecisionConfig.get_quant_method`, and `codebase/tests/quantization/test_modelopt.py` already includes regression coverage for mixed-precision W4A16 dispatch. The local harness in `repro_stdout.log` shows `dispatch W4A16_NVFP4: ModelOptNvFp4W4A16LinearMethod`, so the reported dense-loader crash is not reachable in this checkout.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The current codebase already has the mixed-precision W4A16 dispatch fix and matching regression tests, so the historical `narrow()` out-of-range failure does not reproduce here.
