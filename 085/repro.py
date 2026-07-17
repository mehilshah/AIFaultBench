from __future__ import annotations

import importlib.util
import pathlib
import sys
import traceback
import types


ROOT = pathlib.Path(__file__).resolve().parent


def load_module(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    import torch

    package = types.ModuleType("vit_pytorch")
    package.__path__ = [str(ROOT / "codebase" / "vit_pytorch")]
    sys.modules["vit_pytorch"] = package

    vit_mod = load_module("vit_pytorch.vit", ROOT / "codebase" / "vit_pytorch" / "vit.py")
    mae_mod = load_module("vit_pytorch.mae", ROOT / "codebase" / "vit_pytorch" / "mae.py")

    ViT = vit_mod.ViT
    MAE = mae_mod.MAE

    print(f"torch={torch.__version__}")

    source = (ROOT / "codebase" / "vit_pytorch" / "mae.py").read_text()
    needle = "tokens = tokens + self.encoder.pos_embedding[:, 1:(num_patches + 1)]"
    print("mae_source_has_valid_slice=", needle in source)

    v = ViT(
        image_size=256,
        patch_size=32,
        num_classes=1000,
        dim=1024,
        depth=6,
        heads=8,
        mlp_dim=2048,
    )

    mae = MAE(
        encoder=v,
        masking_ratio=0.75,
        decoder_dim=64,
        decoder_depth=2,
    )

    images = torch.randn(8, 3, 256, 256)
    loss = mae(images)
    print(f"loss={loss.item():.6f}")
    loss.backward()
    print("backward=ok")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        traceback.print_exc()
        raise SystemExit(1)
