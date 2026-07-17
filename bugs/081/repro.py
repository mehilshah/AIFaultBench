import os
import sys
from importlib.util import module_from_spec, spec_from_file_location
import traceback

import torch


def main() -> int:
    codebase_dir = os.path.join(os.path.dirname(__file__), "codebase")
    cross_vit_path = os.path.join(codebase_dir, "vit_pytorch", "cross_vit.py")
    spec = spec_from_file_location("cross_vit", cross_vit_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module spec from {cross_vit_path}")
    cross_vit = module_from_spec(spec)
    sys.modules[spec.name] = cross_vit
    spec.loader.exec_module(cross_vit)
    CrossViT = cross_vit.CrossViT

    model = CrossViT(
        image_size=256,
        num_classes=1000,
        depth=4,
        sm_dim=192,
        sm_patch_size=16,
        sm_enc_depth=2,
        sm_enc_heads=8,
        sm_enc_mlp_dim=2048,
        lg_dim=384,
        lg_patch_size=64,
        lg_enc_depth=3,
        lg_enc_heads=8,
        lg_enc_mlp_dim=2048,
        cross_attn_depth=2,
        cross_attn_heads=8,
        dropout=0.1,
        emb_dropout=0.1,
    )

    img = torch.randn(1, 1, 256, 256)

    try:
        model(img)
    except Exception:
        traceback.print_exc()
        return 1

    print("Unexpected success: CrossViT accepted a 1-channel image.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
