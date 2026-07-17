#!/usr/bin/env python3
import sys

import torch
from torch_geometric.nn import Linear


def main() -> int:
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    torch.manual_seed(12345)

    x = torch.rand((31, 384), device=device)
    layer = Linear(384, 192).to(device)

    outputs = [layer(x) for _ in range(10_000)]

    first_max_diff = max(
        (outputs[0] - out).abs().max().item() for out in outputs
    )
    rest_max_diff = max(
        (outputs[1] - out).abs().max().item() for out in outputs[1:]
    )

    import torch_geometric

    print(f'python={sys.version.split()[0]}')
    print(f'torch={torch.__version__}')
    print(f'torch_geometric={torch_geometric.__version__}')
    print(f'device={device}')
    print(f'cuda_available={torch.cuda.is_available()}')
    print(f'first_max_diff={first_max_diff}')
    print(f'rest_max_diff={rest_max_diff}')

    if first_max_diff != 0.0 or rest_max_diff != 0.0:
        print('reproducible=True')
        return 1

    print('reproducible=False')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
