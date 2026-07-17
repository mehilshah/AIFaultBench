# Bug 502

This folder is a standalone repro bundle for the vLLM mixed-precision NVFP4
dense-load issue described in `bug_report.txt`.

What the upstream report described:
- a dense `nvidia/Qwen3.6-27B-NVFP4` checkpoint
- `quant_algo: "MIXED_PRECISION"` with per-layer `W4A16_NVFP4`
- `mlp.down_proj` falling through to the wrong loader and eventually hitting
  `narrow()` out-of-range on packed 4-bit weights

What this checkout shows:
- `codebase/vllm/model_executor/layers/quantization/modelopt.py` already has a
  dedicated `W4A16_NVFP4` branch in `ModelOptMixedPrecisionConfig.get_quant_method`
  and a sibling `w4a16_nvfp4_config`
- `codebase/tests/quantization/test_modelopt.py` already contains regression
  coverage for the mixed-precision W4A16 dispatch path
- the local `repro.py` harness confirms that:
  - `NVFP4` dispatches to `ModelOptNvFp4LinearMethod`
  - `W4A16_NVFP4` dispatches to `ModelOptNvFp4W4A16LinearMethod`

Conclusion:
- the historical crash is not reproducible in this checkout because the
  relevant mixed-precision dispatch is already fixed here.

How to run:
1. `bash setup_env.sh`
1. `bash run_repro.sh`

Generated artifacts:
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`
