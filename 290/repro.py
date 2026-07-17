#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def bootstrap_timm_namespace():
    timm_pkg = types.ModuleType("timm")
    timm_pkg.__path__ = [str(CODEBASE / "timm")]
    sys.modules.setdefault("timm", timm_pkg)

    layers_pkg = types.ModuleType("timm.layers")
    layers_pkg.__path__ = [str(CODEBASE / "timm" / "layers")]
    layers_pkg.use_reentrant_ckpt = lambda: False
    sys.modules["timm.layers"] = layers_pkg

    models_pkg = types.ModuleType("timm.models")
    models_pkg.__path__ = [str(CODEBASE / "timm" / "models")]
    sys.modules["timm.models"] = models_pkg

    optim_pkg = types.ModuleType("timm.optim")
    optim_pkg.__path__ = [str(CODEBASE / "timm" / "optim")]
    sys.modules["timm.optim"] = optim_pkg

    utils_pkg = types.ModuleType("timm.utils")
    utils_pkg.__path__ = [str(CODEBASE / "timm" / "utils")]
    sys.modules["timm.utils"] = utils_pkg

    manipulate = load_module("timm.models._manipulate", CODEBASE / "timm" / "models" / "_manipulate.py")
    models_pkg.group_parameters = manipulate.group_parameters
    models_pkg.group_modules = manipulate.group_modules
    models_pkg.model_parameters = manipulate.model_parameters

    model_ema = load_module("timm.utils.model_ema", CODEBASE / "timm" / "utils" / "model_ema.py")
    load_module("timm.optim._param_groups", CODEBASE / "timm" / "optim" / "_param_groups.py")
    optim_factory = load_module("timm.optim._optim_factory", CODEBASE / "timm" / "optim" / "_optim_factory.py")
    return manipulate, model_ema, optim_factory


from torch import Tensor, nn  # noqa: E402


EXPECTED_LR_SCALES = [0.81, 0.81, 0.9, 0.9, 1.0, 1.0]


class MyModel(nn.Module):
    def __init__(self, ModelEmaV3):
        super().__init__()
        self.blocks = nn.Sequential(*[nn.Linear(32, 32) for _ in range(3)])
        self.emablocks = ModelEmaV3(nn.Sequential(*[nn.Linear(32, 32) for _ in range(3)]))
        self.emablocks.requires_grad_(False)

    def group_matcher(self, coarse: bool = False):
        return dict(
            blocks=r"^blocks\.(\d+)",
            emablocks=r"^emablocks\.",
        )

    def forward(self, x: Tensor):
        x_ = x
        for blk in self.blocks:
            x = blk(x)

        for emablk in self.emablocks.module:
            x_ = emablk(x_)

        return x, x_


def main() -> int:
    manipulate, model_ema, optim_factory = bootstrap_timm_namespace()

    model = MyModel(model_ema.ModelEmaV3)
    layer_map = manipulate.group_parameters(model, model.group_matcher(coarse=False), reverse=True)
    optimizer = optim_factory.create_optimizer_v2(
        model_or_params=model,
        opt="adamw",
        lr=1e-3,
        weight_decay=0.05,
        layer_decay=0.9,
    )

    actual_lr_scales = [group["lr_scale"] for group in optimizer.param_groups]
    named_params = list(model.named_parameters())
    trainable_params = [(name, p) for name, p in named_params if p.requires_grad]

    print("named_parameters:", len(named_params))
    print("trainable_parameters:", len(trainable_params))
    print("layer_map:", json.dumps(layer_map, sort_keys=True))
    print("param_groups:", len(optimizer.param_groups))
    print("actual_lr_scales:", actual_lr_scales)
    print("expected_lr_scales:", EXPECTED_LR_SCALES)

    if actual_lr_scales != EXPECTED_LR_SCALES:
        print("BUG_REPRODUCED: frozen parameters were counted when assigning layer decay scales.")
        return 1

    print("NO_BUG: actual lr scales match the expected sequence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
