import sys
import traceback

import torch
from timm.models.eva import Eva


def run_case(batch_size: int) -> None:
    print(f"Running Eva(batch_size={batch_size}, patch_drop_rate=0.75, use_rot_pos_emb=True)")
    model = Eva(patch_drop_rate=0.75, use_rot_pos_emb=True)
    model.train()
    x = torch.randn(batch_size, 3, 224, 224)
    y = model(x)
    print(f"Output shape: {tuple(y.shape)}")


def main() -> int:
    print(f"torch {torch.__version__}")

    try:
        run_case(1)
    except Exception:
        print("Unexpected failure for batch_size=1", file=sys.stderr)
        traceback.print_exc()
        return 1

    try:
        run_case(8)
    except Exception as exc:
        print(f"Observed failure for batch_size=8: {exc}", file=sys.stderr)
        traceback.print_exc()
        return 1

    print("No failure observed for batch_size=8; bug not reproduced.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
