import traceback

import torch

import torch_geometric.typing as typing
from torch_geometric.data import Data
from torch_geometric.loader import NeighborLoader


def main() -> int:
    print(f"torch={torch.__version__}")
    print(f"WITH_PYG_LIB={typing.WITH_PYG_LIB}")
    print(f"WITH_TORCH_SPARSE={typing.WITH_TORCH_SPARSE}")

    data = Data(
        x=torch.arange(12, dtype=torch.float32).view(4, 3),
        edge_index=torch.tensor([[0, 1, 2, 3], [1, 2, 3, 0]]),
        train_mask=torch.tensor([True, True, False, False]),
        y=torch.tensor([0, 1, 0, 1]),
    )

    loader = NeighborLoader(
        data,
        input_nodes=data.train_mask,
        num_neighbors=[2, 2],
        batch_size=2,
        directed=False,
    )
    print(f"loader={loader}")

    try:
        next(iter(loader))
    except Exception as exc:
        print(f"{type(exc).__name__}: {exc}")
        traceback.print_exc()
        return 1

    print("unexpected success")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
