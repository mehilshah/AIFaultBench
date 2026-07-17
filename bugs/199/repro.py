import torch

from torch_geometric.nn import ChebConv
from torch_geometric.utils import get_num_hops, to_undirected


def main() -> int:
    # Deterministic weights make the hop-count mismatch stable across runs.
    x = torch.tensor([1, 0, 0, 0, 0, 0], dtype=torch.float32).unsqueeze(1)
    edge_index = to_undirected(
        torch.tensor([[0, 1, 2, 3, 4], [1, 2, 3, 4, 5]], dtype=torch.long))
    edge_weight = torch.ones(edge_index.size(1))

    model = ChebConv(1, 1, K=3)
    with torch.no_grad():
        for lin in model.lins:
            lin.weight.fill_(1.0)
        model.bias.zero_()

    y = model(x, edge_index, edge_weight)
    reported_hops = get_num_hops(model)
    actual_hops = torch.count_nonzero(y).item() - 1

    print(f"get_num_hops: {reported_hops}")
    print(f"actual hops: {actual_hops}")
    print(f"output: {y.flatten().tolist()}")

    if reported_hops == 1 and actual_hops == 2:
        print(
            "BUG REPRODUCED: get_num_hops counts MessagePassing layers rather "
            "than effective receptive-field hops for ChebConv(K=3).",
        )
        return 1

    print("BUG NOT REPRODUCED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
