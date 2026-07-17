#!/usr/bin/env python3
"""Minimal repro for Detectron2 Instances integer indexing bug."""

from __future__ import annotations

import os
import importlib.util
import types
import sys
import traceback


def main() -> int:
    repo_root = os.path.dirname(os.path.abspath(__file__))
    codebase_root = os.path.join(repo_root, "codebase")

    import torch

    # Load only the pieces needed for the bug. The full detectron2 package
    # imports compiled extensions that are not required for this repro.
    detectron2_pkg = types.ModuleType("detectron2")
    detectron2_pkg.__path__ = [os.path.join(codebase_root, "detectron2")]
    sys.modules["detectron2"] = detectron2_pkg

    layers_mod = types.ModuleType("detectron2.layers")
    layers_mod.cat = lambda tensors, dim=0: tensors[0] if len(tensors) == 1 else torch.cat(tensors, dim)
    sys.modules["detectron2.layers"] = layers_mod

    instances_path = os.path.join(codebase_root, "detectron2", "structures", "instances.py")
    spec = importlib.util.spec_from_file_location("detectron2.structures.instances", instances_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load Instances module from {instances_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    Instances = module.Instances

    instances = Instances((10, 10), scores=torch.tensor([0.9]))
    print(f"instances_len={len(instances)}")
    print(f"field_shape={tuple(instances.get('scores').shape)}")
    print("indexing_instances[0] ...")

    try:
        indexed = instances[0]
    except Exception as exc:  # noqa: BLE001 - we want the full traceback in logs
        print(f"caught_exception={type(exc).__name__}: {exc}")
        traceback.print_exc()
        return 1

    print(f"unexpected_success={indexed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
