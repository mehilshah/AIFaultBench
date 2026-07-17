import torch
from torch import nn

import torch_geometric
import torch_geometric.typing as tgtyping
from torch_geometric.nn import knn_graph


class SampleModule(nn.Module):
    def forward(self, x: torch.Tensor, position: torch.Tensor) -> torch.Tensor:
        del x
        return knn_graph(position.squeeze(0), k=20, flow='target_to_source')


def main() -> None:
    model = SampleModule().eval()
    print(f'torch {torch.__version__}')
    print(f'torch_geometric {torch_geometric.__version__}')
    print(f'pyg_lib available {tgtyping.WITH_PYG_LIB}')
    print(f'knn available {tgtyping.WITH_KNN}')
    torch.export.export(
        model,
        args=(torch.randn(10, 10), torch.randn(10, 10)),
        strict=False,
    )


if __name__ == '__main__':
    main()
