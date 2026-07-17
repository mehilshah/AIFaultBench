import os

import networkx as nx
import torch
import torch.nn as nn
import lightning_fabric

import gconv_gru


graph_lists = [
    [
        "13010065",
        "13011000",
        "13011500",
        "13013650",
        "13018750",
        "13022500",
        "13032500",
        "13037500",
        "13038500",
        "13057000",
        "13057155",
        "13060000",
        "13062500",
        "13069500",
    ],
    [
        "13014500",
        "13015000",
        "13018750",
        "13022500",
        "13032500",
        "13037500",
        "13038500",
        "13057000",
        "13057155",
        "13060000",
        "13062500",
        "13069500",
    ],
    [
        "13011900",
        "13013650",
        "13018750",
        "13022500",
        "13032500",
        "13037500",
        "13038500",
        "13057000",
        "13057155",
        "13060000",
        "13062500",
        "13069500",
    ],
    [
        "13018300",
        "13018350",
        "13018750",
        "13022500",
        "13032500",
        "13037500",
        "13038500",
        "13057000",
        "13057155",
        "13060000",
        "13062500",
        "13069500",
    ],
    [
        "13016450",
        "13018750",
        "13022500",
        "13032500",
        "13037500",
        "13038500",
        "13057000",
        "13057155",
        "13060000",
        "13062500",
        "13069500",
    ],
    [
        "13016305",
        "13018750",
        "13022500",
        "13032500",
        "13037500",
        "13038500",
        "13057000",
        "13057155",
        "13060000",
        "13062500",
        "13069500",
    ],
    [
        "13046995",
        "13047500",
        "13047600",
        "13049500",
        "13050500",
        "13056500",
        "13057000",
        "13057155",
        "13060000",
        "13062500",
        "13069500",
    ],
    [
        "13039500",
        "13042500",
        "13046000",
        "13050500",
        "13056500",
        "13057000",
        "13057155",
        "13060000",
        "13062500",
        "13069500",
    ],
    [
        "13052200",
        "13055000",
        "13055250",
        "13056500",
        "13057000",
        "13057155",
        "13060000",
        "13062500",
        "13069500",
    ],
    [
        "13027500",
        "13032500",
        "13037500",
        "13038500",
        "13057000",
        "13057155",
        "13060000",
        "13062500",
        "13069500",
    ],
    [
        "13023000",
        "13032500",
        "13037500",
        "13038500",
        "13057000",
        "13057155",
        "13060000",
        "13062500",
        "13069500",
    ],
    [
        "13055340",
        "13056500",
        "13057000",
        "13057155",
        "13060000",
        "13062500",
        "13069500",
    ],
    ["13057940", "13058000", "13068500", "13069500"],
    ["13063000", "13066000", "13068500", "13069500"],
]


class RepModel(nn.Module):
    def __init__(self, edge_index):
        super().__init__()
        self.gcgru0 = gconv_gru.GConvGRU(in_channels=24, out_channels=32, K=5)
        self.edge_index = edge_index

    def forward(self, x):
        return self.gcgru0(x, self.edge_index)


def gen_nx_graph(basin_path_lists):
    dg = nx.DiGraph()
    for path in basin_path_lists:
        nx.add_path(dg, path)
    node_mapping = {node: idx for idx, node in enumerate(dg.nodes)}
    edges = [(node_mapping[u], node_mapping[v]) for u, v in dg.edges]
    return dg, edges


if __name__ == "__main__":
    os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
    os.environ["TORCH_USE_CUDA_DSA"] = "1"

    total_fab = lightning_fabric.Fabric(devices=[0, 1], strategy="ddp")
    total_fab.launch()

    G, basin_edges = gen_nx_graph(graph_lists)
    edge_index = torch.tensor(basin_edges, device=total_fab.device).t().contiguous()
    model = total_fab.setup_module(RepModel(edge_index))
    test_tensor = torch.randn(16, len(G), 24, device=total_fab.device)
    output = model(test_tensor)
    print(output)
