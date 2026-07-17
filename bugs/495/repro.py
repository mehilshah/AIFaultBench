#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'codebase'))

import torch
from torch import nn

from torch_geometric.explain import Explainer, PGExplainer
from torch_geometric.explain.config import ModelConfig
from torch_geometric.nn import GCNConv


class GCN(nn.Module):
    def __init__(self, model_config: ModelConfig):
        super().__init__()
        self.model_config = model_config
        self.conv1 = GCNConv(4, 16)
        self.conv2 = GCNConv(16, 1)

    def forward(self, x, edge_index, batch=None):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x.mean(dim=0, keepdim=True)


def main() -> int:
    if not torch.cuda.is_available():
        raise SystemExit('CUDA is not available in this environment.')

    device = torch.device('cuda')
    model_config = ModelConfig(
        mode='binary_classification',
        task_level='graph',
        return_type='raw',
    )

    model = GCN(model_config).to(device)
    explainer = Explainer(
        model=model,
        algorithm=PGExplainer(epochs=2),
        explanation_type='phenomenon',
        edge_mask_type='object',
        model_config=model_config,
    )

    x = torch.randn(8, 4, device=device)
    edge_index = torch.tensor(
        [
            [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7],
            [1, 0, 2, 1, 3, 2, 4, 3, 5, 4, 6, 5, 7, 6],
        ],
        device=device,
    )
    target = torch.randint(2, (1,), device=device)

    print(f'torch={torch.__version__}')
    print(f'model_device={next(model.parameters()).device}')
    print(
        'explainer_mlp_device='
        f'{next(explainer.algorithm.mlp.parameters()).device}'
    )
    print(f'input_device={x.device}')
    print('calling PGExplainer.train() without moving the algorithm to cuda')

    # This should fail exactly where the issue report describes: the explainer
    # MLP stays on CPU while the graph embeddings are on CUDA.
    explainer.algorithm.train(
        epoch=0,
        model=model,
        x=x,
        edge_index=edge_index,
        target=target,
    )

    print('unexpected success')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
