from __future__ import annotations

import importlib.util
import pathlib

import torch


ROOT_DIR = pathlib.Path(__file__).resolve().parent
MODEL_PATH = ROOT_DIR / "codebase" / "vit_pytorch" / "na_vit_nested_tensor_3d.py"


def load_model_class():
    spec = importlib.util.spec_from_file_location("na_vit_nested_tensor_3d", MODEL_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load module from {MODEL_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.NaViT


def main():
    NaViT = load_model_class()

    torch.manual_seed(0)

    model = NaViT(
        image_size=32,
        max_frames=4,
        patch_size=16,
        frame_patch_size=2,
        num_classes=10,
        dim=16,
        depth=1,
        heads=2,
        mlp_dim=32,
        dropout=0.0,
        emb_dropout=0.0,
        token_dropout_prob=0.0,
    )
    model.train()

    volumes = [
        torch.randn(3, 2, 32, 32, requires_grad=True),
        torch.randn(3, 4, 16, 32, requires_grad=True),
    ]

    out = model(volumes)
    print(f"forward_ok shape={tuple(out.shape)}")
    out.sum().backward()
    print("backward_ok")


if __name__ == "__main__":
    main()
