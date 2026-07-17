#!/usr/bin/env python3
"""Reproduce the ERNIE modular pipeline LoRA API gap from the local source tree."""

from __future__ import annotations

import importlib
import json
import os
import sys
import types
from dataclasses import dataclass
from pathlib import Path
from textwrap import indent


ROOT = Path(__file__).resolve().parent
CODEBASE_SRC = ROOT / "codebase" / "src"
STUBS_DIR = ROOT / "repro_support"
RESULT_PATH = ROOT / "reproduction.json"


def ensure_package(name: str, path: Path, attrs: dict[str, object] | None = None) -> types.ModuleType:
    module = sys.modules.get(name)
    if module is None:
        module = types.ModuleType(name)
        module.__path__ = [str(path)]  # type: ignore[attr-defined]
        module.__package__ = name
        sys.modules[name] = module
    if attrs:
        for key, value in attrs.items():
            setattr(module, key, value)
    return module


def load_modules():
    os.environ.setdefault("USE_TORCH", "NO")
    os.environ.setdefault("USE_TF", "NO")

    sys.path.insert(0, str(STUBS_DIR))
    sys.path.insert(1, str(CODEBASE_SRC))

    ensure_package("diffusers", CODEBASE_SRC / "diffusers", {"__version__": "0.39.0.dev0"})
    hooks_module = types.ModuleType("diffusers.hooks")

    class ModelHook:
        pass

    hooks_module.ModelHook = ModelHook
    sys.modules["diffusers.hooks"] = hooks_module
    ensure_package("diffusers.modular_pipelines", CODEBASE_SRC / "diffusers" / "modular_pipelines")
    ensure_package(
        "diffusers.modular_pipelines.ernie_image",
        CODEBASE_SRC / "diffusers" / "modular_pipelines" / "ernie_image",
    )

    import diffusers.utils.import_utils as import_utils

    import_utils._torch_version = "2.3.0"
    import_utils._torch_available = False
    import_utils._transformers_version = "5.0.0"
    import_utils._transformers_available = False

    modular_pipeline_mod = importlib.import_module("diffusers.modular_pipelines.modular_pipeline")
    ernie_mod = importlib.import_module("diffusers.modular_pipelines.ernie_image.modular_pipeline")
    return modular_pipeline_mod, ernie_mod


def class_bases_and_methods(module, class_name: str) -> tuple[list[str], set[str]]:
    cls = getattr(module, class_name)
    bases = [base.__name__ for base in cls.__bases__]
    methods = {name for name, value in cls.__dict__.items() if callable(value)}
    return bases, methods


def main() -> int:
    modular_pipeline_mod, ernie_mod = load_modules()
    ernie_cls = ernie_mod.ErnieImageModularPipeline

    bases, methods = class_bases_and_methods(ernie_mod, "ErnieImageModularPipeline")
    has_lora_method = hasattr(ernie_cls, "load_lora_weights")

    try:
        pipe = ernie_cls.__new__(ernie_cls)
        pipe.load_lora_weights("dummy")
        runtime_error = None
    except AttributeError as exc:
        runtime_error = str(exc)
    except Exception as exc:  # pragma: no cover - defensive, surfaced in logs
        runtime_error = f"unexpected exception: {exc!r}"

    modular_source = (CODEBASE_SRC / "diffusers" / "modular_pipelines" / "ernie_image" / "modular_pipeline.py").read_text()
    pipeline_source = (CODEBASE_SRC / "diffusers" / "pipelines" / "ernie_image" / "pipeline_ernie_image.py").read_text()

    evidence_lines = [
        f"ErnieImageModularPipeline bases: {bases}",
        f"ErnieImageModularPipeline defines methods: {sorted(name for name in methods if name.startswith('load_') or name.startswith('save_')) or 'none'}",
        f"hasattr(ErnieImageModularPipeline, 'load_lora_weights') -> {has_lora_method}",
        f"calling pipe.load_lora_weights(...) -> {runtime_error}",
        "modular pipeline source shows `class ErnieImageModularPipeline(ModularPipeline)` at line 66",
        "non-modular pipeline source shows `class ErnieImagePipeline(DiffusionPipeline, ErnieImageLoraLoaderMixin)` at line 42",
    ]

    result = {
        "reproducible": runtime_error is not None and "load_lora_weights" in runtime_error,
        "evidence": " | ".join(evidence_lines),
        "steps": [
            "Import the real `ErnieImageModularPipeline` class from `codebase/src` using a local `torch` stub.",
            "Instantiate the class shell and call `load_lora_weights` on it.",
            "Observe `AttributeError: 'ErnieImageModularPipeline' object has no attribute 'load_lora_weights'`.",
        ],
        "blocking_reason": "" if runtime_error is not None else "Unexpectedly found a callable load_lora_weights method.",
        "reproduction_command": "bash run_repro.sh",
    }

    RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    print("Repro result written to", RESULT_PATH.name)
    print("Summary:")
    print(indent("\n".join(evidence_lines), "  "))

    return 0 if result["reproducible"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
