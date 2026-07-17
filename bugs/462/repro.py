from torch import Tensor
from torch_geometric.nn import MessagePassing


class Tmp(MessagePassing):
    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__(aggr='add')

    def forward(self, x: Tensor, edge_index: Tensor) -> None:
        return None

    def message(self, x_j: Tensor, edge_attr: Tensor | None = None) -> None:
        return None


tmp = Tmp(123, 123)
print(tmp)
