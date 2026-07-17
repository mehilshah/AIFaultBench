#!/usr/bin/env python3
"""Minimal reproducer for the GLEM pseudo-label None crash."""

from __future__ import annotations

import importlib.util
import pathlib
import sys
import types


ROOT = pathlib.Path(__file__).resolve().parent
GLEM_PATH = ROOT / "codebase" / "torch_geometric" / "nn" / "models" / "glem.py"


def install_torch_stub() -> None:
    torch = types.ModuleType("torch")
    torch.Tensor = object
    torch.dtype = object
    torch.bfloat16 = "bfloat16"
    torch.device = lambda name=None: name
    torch.no_grad = lambda: (lambda fn: fn)
    torch.cuda = types.SimpleNamespace(
        is_available=lambda: False,
        get_device_name=lambda *_: "cpu",
        empty_cache=lambda: None,
        memory_allocated=lambda: 0,
        max_memory_allocated=lambda: 0,
    )

    class Module:
        pass

    class CrossEntropyLoss:
        def __init__(self, *args, **kwargs):
            pass

    nn_mod = types.ModuleType("torch.nn")
    nn_mod.Module = Module
    nn_mod.CrossEntropyLoss = CrossEntropyLoss
    nn_mod.functional = types.ModuleType("torch.nn.functional")

    optim_mod = types.ModuleType("torch.optim")
    optim_mod.Optimizer = object

    torch.nn = nn_mod
    torch.optim = optim_mod

    sys.modules["torch"] = torch
    sys.modules["torch.nn"] = nn_mod
    sys.modules["torch.nn.functional"] = nn_mod.functional
    sys.modules["torch.optim"] = optim_mod


def install_tqdm_stub() -> None:
    tqdm_mod = types.ModuleType("tqdm")
    tqdm_mod.tqdm = lambda *args, **kwargs: types.SimpleNamespace(
        set_description=lambda *a, **k: None,
        update=lambda *a, **k: None,
        close=lambda *a, **k: None,
    )
    sys.modules["tqdm"] = tqdm_mod


def install_torch_geometric_stub() -> None:
    tg_mod = types.ModuleType("torch_geometric")
    loader_mod = types.ModuleType("torch_geometric.loader")
    loader_mod.DataLoader = object
    loader_mod.NeighborLoader = object
    nn_mod = types.ModuleType("torch_geometric.nn")
    models_mod = types.ModuleType("torch_geometric.nn.models")
    models_mod.GraphSAGE = object
    models_mod.basic_gnn = types.SimpleNamespace()

    tg_mod.loader = loader_mod
    tg_mod.nn = nn_mod
    nn_mod.models = models_mod

    sys.modules["torch_geometric"] = tg_mod
    sys.modules["torch_geometric.loader"] = loader_mod
    sys.modules["torch_geometric.nn"] = nn_mod
    sys.modules["torch_geometric.nn.models"] = models_mod


def load_glem_module():
    spec = importlib.util.spec_from_file_location("glem_module", GLEM_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> None:
    print(f"Loading real GLEM implementation from: {GLEM_PATH}")
    print("Reproducing the `train_without_ext_pred=True` failure path.")
    print("This mirrors `examples/llm/glem.py` passing ext_pseudo_labels=None")
    print("into `GLEM.train()` during GNN pretraining.")

    install_torch_stub()
    install_tqdm_stub()
    install_torch_geometric_stub()

    glem_module = load_glem_module()
    GLEM = glem_module.GLEM

    model = GLEM.__new__(GLEM)
    model.device = "cpu"
    model.train_gnn = lambda *args, **kwargs: (0.0, 0.0)
    model.train_lm = lambda *args, **kwargs: (0.0, 0.0)

    # The bug is triggered before the phase-specific training code runs.
    model.train("gnn", object(), object(), None, 1, False, False)


if __name__ == "__main__":
    main()

