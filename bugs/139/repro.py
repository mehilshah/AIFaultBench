#!/usr/bin/env python3
from __future__ import annotations

import platform
import sys

import torch

from timm.models.vision_transformer import Mlp


def main() -> int:
    torch.manual_seed(0)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(0)

    print(f"python={sys.version.split()[0]}")
    print(f"platform={platform.platform()}")
    print(f"torch={torch.__version__}")
    print(f"cuda_available={torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"device={torch.cuda.get_device_name(0)}")
        print(f"capability={torch.cuda.get_device_capability(0)}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    x = (torch.rand(1, 499, 1280, device=device) * 1000).repeat(2, 1, 1)
    print(f"inputs_equal={x[0].equal(x[1])}")

    mlp = Mlp(
        in_features=1280,
        hidden_features=5120,
        act_layer=torch.nn.GELU,
        drop=0.0,
    ).to(device)
    mlp.eval()

    with torch.no_grad():
        result_single = mlp(x[:1])
        result_double = mlp(x[:2])

    same_batch = result_double[0].equal(result_double[1])
    cross_batch = result_single[0].equal(result_double[0])
    max_abs_diff = (result_single[0] - result_double[0]).abs().max().item()

    print(f"double_rows_equal={same_batch}")
    print(f"single_vs_double_equal={cross_batch}")
    print(f"max_abs_diff={max_abs_diff}")

    if same_batch and not cross_batch:
        print("BUG_REPRODUCED=True")
        return 0

    print("BUG_REPRODUCED=False")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
