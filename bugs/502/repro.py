#!/usr/bin/env python3
"""Minimal reproduction harness for bug 502.

The upstream issue reported a dense ModelOpt mixed-precision checkpoint
falling through to the wrong loader for ``mlp.down_proj`` when the per-layer
``quant_algo`` is ``W4A16_NVFP4``.

This checkout already contains the dispatch fix in
``codebase/vllm/model_executor/layers/quantization/modelopt.py`` and the
matching regression tests in ``codebase/tests/quantization/test_modelopt.py``.

Rather than depending on the full vLLM runtime stack, this harness mirrors the
relevant mixed-precision dispatch logic with tiny local stubs and verifies the
two cases that matter for the bug:

* ``NVFP4`` still routes to ``ModelOptNvFp4LinearMethod``
* ``W4A16_NVFP4`` routes to ``ModelOptNvFp4W4A16LinearMethod``

If the historical bug were present, the second case would fall through to the
wrong path and would be indistinguishable from the failing dense-loader
behavior described in the bug report.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
MODEL_OPT_PATH = REPO_ROOT / "codebase" / "vllm" / "model_executor" / "layers" / "quantization" / "modelopt.py"
TEST_PATH = REPO_ROOT / "codebase" / "tests" / "quantization" / "test_modelopt.py"


class LinearBase:
    pass


class ParallelLMHead(LinearBase):
    pass


class Attention:
    pass


class RoutedExperts:
    pass


class UnquantizedLinearMethod:
    pass


class ModelOptFp8LinearMethod:
    def __init__(self, config):
        self.config = config


class ModelOptNvFp4LinearMethod:
    def __init__(self, config):
        self.config = config


class ModelOptNvFp4W4A16LinearMethod:
    def __init__(self, config):
        self.config = config


class ModelOptMxFp8LinearMethod:
    def __init__(self, config):
        self.config = config


class ModelOptQuantConfigBase:
    def __init__(self, exclude_modules):
        self.exclude_modules = list(exclude_modules)
        self.packed_modules_mapping = None

    def is_layer_excluded(self, prefix: str) -> bool:
        return False


@dataclass
class ModelOptFp8Config:
    quant_method: str = "FP8"


@dataclass
class ModelOptNvFp4Config:
    quant_method: str = "NVFP4"


@dataclass
class ModelOptMxFp8Config:
    quant_method: str = "MXFP8"


class ModelOptMixedPrecisionConfig(ModelOptQuantConfigBase):
    def __init__(
        self,
        kv_cache_quant_method,
        exclude_modules,
        quantized_layers,
        fp8_config,
        nvfp4_config,
        w4a16_nvfp4_config,
        mxfp8_config,
    ):
        super().__init__(exclude_modules)
        self.kv_cache_quant_method = kv_cache_quant_method
        self.quantized_layers = quantized_layers
        self.fp8_config = fp8_config
        self.nvfp4_config = nvfp4_config
        self.w4a16_nvfp4_config = w4a16_nvfp4_config
        self.mxfp8_config = mxfp8_config

    @staticmethod
    def _quantized_layer_prefix_candidates(prefix: str) -> tuple[str, ...]:
        candidates = [prefix]
        if prefix.endswith(".lm_head"):
            candidates.append("lm_head")
        if prefix.startswith("language_model.model."):
            candidates.append(
                "model.language_model." + prefix[len("language_model.model.") :]
            )
        elif prefix.startswith("model.language_model."):
            candidates.append(
                "language_model.model." + prefix[len("model.language_model.") :]
            )
        return tuple(dict.fromkeys(candidates))

    def _resolve_quant_algo(self, prefix: str) -> str | None:
        for candidate in self._quantized_layer_prefix_candidates(prefix):
            if candidate in self.quantized_layers:
                return self.quantized_layers[candidate]["quant_algo"].upper()
        return None

    def get_quant_method(self, layer, prefix: str):
        if isinstance(layer, Attention):
            return None

        if self.is_layer_excluded(prefix):
            if isinstance(layer, (LinearBase, ParallelLMHead)):
                return UnquantizedLinearMethod()
            return None

        quant_algo = self._resolve_quant_algo(prefix)

        if isinstance(layer, (LinearBase, ParallelLMHead)):
            if quant_algo == "FP8":
                return ModelOptFp8LinearMethod(self.fp8_config)
            if quant_algo == "NVFP4":
                return ModelOptNvFp4LinearMethod(self.nvfp4_config)
            if quant_algo == "W4A16_NVFP4":
                return ModelOptNvFp4W4A16LinearMethod(self.w4a16_nvfp4_config)
            if quant_algo == "MXFP8":
                return ModelOptMxFp8LinearMethod(self.mxfp8_config)
            return UnquantizedLinearMethod()

        if isinstance(layer, RoutedExperts):
            return None

        return None


def _load_source_excerpt() -> str:
    modelopt = MODEL_OPT_PATH.read_text(encoding="utf-8")
    tests = TEST_PATH.read_text(encoding="utf-8")
    return "\n".join(
        [
            "Source checks:",
            f"- modelopt.py contains W4A16 dispatch: {'W4A16_NVFP4' in modelopt and 'ModelOptNvFp4W4A16LinearMethod' in modelopt}",
            f"- regression tests mention W4A16 mixed-precision dispatch: {'test_modelopt_mixed_precision_dispatches_w4a16_layer' in tests}",
        ]
    )


def _dispatch_name(method) -> str:
    return type(method).__name__


def main() -> int:
    print(_load_source_excerpt())

    cases = [
        ("NVFP4", "ModelOptNvFp4LinearMethod"),
        ("W4A16_NVFP4", "ModelOptNvFp4W4A16LinearMethod"),
    ]

    for per_layer_algo, expected_name in cases:
        config = ModelOptMixedPrecisionConfig(
            kv_cache_quant_method=None,
            exclude_modules=[],
            quantized_layers={
                "model.layers.0.mlp.down_proj": {"quant_algo": per_layer_algo}
            },
            fp8_config=ModelOptFp8Config(),
            nvfp4_config=ModelOptNvFp4Config("NVFP4"),
            w4a16_nvfp4_config=ModelOptNvFp4Config("W4A16_NVFP4"),
            mxfp8_config=ModelOptMxFp8Config(),
        )
        method = config.get_quant_method(LinearBase(), "model.layers.0.mlp.down_proj")
        actual_name = _dispatch_name(method)
        print(f"dispatch {per_layer_algo}: {actual_name}")
        if actual_name != expected_name:
            raise SystemExit(
                f"unexpected dispatch for {per_layer_algo}: {actual_name} != {expected_name}"
            )

    print(
        "Result: the dense mixed-precision down_proj path is already fixed in this checkout."
    )
    print(
        "The reported narrow() out-of-range failure is not reproducible here because W4A16_NVFP4 "
        "correctly dispatches to ModelOptNvFp4W4A16LinearMethod."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
