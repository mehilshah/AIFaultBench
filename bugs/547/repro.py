#!/usr/bin/env python3
"""Minimal reproduction for DeepSpeed issue 7733.

The checked-in source uses ``torch.sqrt`` on a Python float in
``scale_lr(base_batch_size, batch_size, ...)`` when ``method == "sqrt"``.
This script loads the source file directly, stubs the unrelated DeepSpeed
imports it pulls in at module load time, and calls the buggy helper.
"""

from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
SOURCE_FILE = ROOT_DIR / "codebase" / "deepspeed" / "runtime" / "data_pipeline" / "data_sampling" / "variable_batch_size_and_lr.py"


def _ensure_module(name: str) -> types.ModuleType:
    module = sys.modules.get(name)
    if module is None:
        module = types.ModuleType(name)
        if "." not in name:
            module.__path__ = []  # type: ignore[attr-defined]
        sys.modules[name] = module
    return module


def install_import_stubs() -> None:
    # Build just enough of the DeepSpeed package tree to import the target file.
    for name in [
        "deepspeed",
        "deepspeed.utils",
        "deepspeed.runtime",
        "deepspeed.runtime.pipe",
        "deepspeed.runtime.pipe.engine",
        "deepspeed.runtime.data_pipeline",
        "deepspeed.runtime.data_pipeline.constants",
        "deepspeed.runtime.data_pipeline.data_sampling",
        "deepspeed.runtime.data_pipeline.data_sampling.indexed_dataset",
        "deepspeed.runtime.data_pipeline.data_sampling.data_analyzer",
    ]:
        _ensure_module(name)

    sys.modules["deepspeed"].utils = sys.modules["deepspeed.utils"]
    sys.modules["deepspeed"].runtime = sys.modules["deepspeed.runtime"]
    sys.modules["deepspeed.runtime"].pipe = sys.modules["deepspeed.runtime.pipe"]
    sys.modules["deepspeed.runtime"].data_pipeline = sys.modules["deepspeed.runtime.data_pipeline"]
    sys.modules["deepspeed.runtime.pipe"].engine = sys.modules["deepspeed.runtime.pipe.engine"]
    sys.modules["deepspeed.runtime.data_pipeline"].constants = sys.modules["deepspeed.runtime.data_pipeline.constants"]
    sys.modules["deepspeed.runtime.data_pipeline"].data_sampling = sys.modules[
        "deepspeed.runtime.data_pipeline.data_sampling"
    ]
    sys.modules["deepspeed.runtime.data_pipeline.data_sampling"].indexed_dataset = sys.modules[
        "deepspeed.runtime.data_pipeline.data_sampling.indexed_dataset"
    ]
    sys.modules["deepspeed.runtime.data_pipeline.data_sampling"].data_analyzer = sys.modules[
        "deepspeed.runtime.data_pipeline.data_sampling.data_analyzer"
    ]

    sys.modules["deepspeed.utils"].logger = types.SimpleNamespace(info=print, warning=print)
    sys.modules["deepspeed.runtime.pipe.engine"].PipelineEngine = type("PipelineEngine", (), {})
    sys.modules["deepspeed.runtime.data_pipeline.data_sampling.indexed_dataset"].MMapIndexedDataset = object
    sys.modules["deepspeed.runtime.data_pipeline.data_sampling.data_analyzer"].DistributedDataAnalyzer = object


def load_target_module():
    install_import_stubs()
    spec = importlib.util.spec_from_file_location("variable_batch_size_and_lr", SOURCE_FILE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load spec for {SOURCE_FILE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    module = load_target_module()
    print(f"Loaded: {module.__name__}")
    print("Calling scale_lr(2, 4, 1.0, 'sqrt') from the checked-in source file...")
    module.scale_lr(2, 4, 1.0, "sqrt")


if __name__ == "__main__":
    main()
