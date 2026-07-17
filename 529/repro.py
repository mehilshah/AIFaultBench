import argparse
import os
import random
from dataclasses import dataclass

import torch
import torch.distributed as dist
import torch.multiprocessing as mp
import torch.nn.functional as F
from torch.nn import BatchNorm1d, Dropout, LayerNorm, Linear, ModuleList, ReLU, Sequential
from torch.utils.data import Dataset, DistributedSampler

from torch_geometric.data import Data
from torch_geometric.loader import DataLoader
from torch_geometric.nn import GraphConv, global_add_pool, global_max_pool, global_mean_pool


@dataclass(frozen=True)
class Config:
    dim_in: int = 151
    dim_h: int = 256
    dim_out: int = 1
    num_layers: int = 4
    num_graphs: int = 8
    num_nodes: int = 148
    batch_size: int = 2
    world_size: int = 2
    force_cpu: bool = False


class SyntheticGraphDataset(Dataset):
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.items = [self._make_graph(i) for i in range(cfg.num_graphs)]

    def _make_graph(self, graph_id: int) -> Data:
        num_nodes = self.cfg.num_nodes
        src = torch.arange(num_nodes, dtype=torch.long)
        dst = (src + 1) % num_nodes
        edge_index = torch.stack([torch.cat([src, dst]), torch.cat([dst, src])])
        edge_attr = torch.randn(edge_index.size(1), 1)
        x = torch.randn(num_nodes, self.cfg.dim_in)
        y = torch.tensor([graph_id % 2], dtype=torch.float)
        return Data(x=x, edge_index=edge_index, edge_attr=edge_attr, y=y)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, idx):
        return self.items[idx]


class GraphConvNetwork(torch.nn.Module):
    """Reported model shape, adapted for a local distributed repro."""

    def __init__(self, dim_in=151, dim_h: int = 256, dim_out: int = 1, num_layers: int = 4):
        super().__init__()
        self.convs = ModuleList()
        self.convs.append(GraphConv(dim_in, dim_h))
        self.ln = LayerNorm(dim_h)
        for _ in range(num_layers - 1):
            self.convs.append(GraphConv(dim_h, dim_h))

        concat_size = dim_h * 3 * num_layers
        dim_inter_0 = min(1024, max(2, concat_size // 2))
        dim_inter_1 = max(2, dim_inter_0 // 2)

        self.linear = Sequential(
            Linear(concat_size, dim_inter_0),
            BatchNorm1d(dim_inter_0),
            ReLU(),
            Linear(dim_inter_0, dim_inter_1),
            Dropout(0.5),
            ReLU(),
            Linear(dim_inter_1, dim_out),
        )
        self.num_layers = num_layers

    def forward(self, x, edge_index, edge_attr, batch):
        if torch.any(edge_attr < 0):
            edge_attr = torch.abs(edge_attr)

        global_repr = []
        for i, conv in enumerate(self.convs):
            x = conv(x, edge_index)
            emb = x
            x = F.leaky_relu(x)
            x = F.dropout(x, p=0.1, training=self.training)
            if i != self.num_layers - 1:
                x = self.ln(x)

            global_repr.append(global_max_pool(x, batch))
            global_repr.append(global_add_pool(x, batch))
            global_repr.append(global_mean_pool(x, batch))

        h = torch.cat(global_repr, dim=1)
        h = self.linear(h)
        return emb, torch.sigmoid(h)


def _setup_process_group(rank: int, world_size: int, use_cuda: bool):
    os.environ.setdefault("MASTER_ADDR", "127.0.0.1")
    os.environ.setdefault("MASTER_PORT", "12355")
    backend = "nccl" if use_cuda else "gloo"
    dist.init_process_group(backend=backend, rank=rank, world_size=world_size)


def run_worker(rank: int, world_size: int, cfg: Config):
    use_cuda = (
        not cfg.force_cpu
        and torch.cuda.is_available()
        and torch.cuda.device_count() >= world_size
    )
    _setup_process_group(rank, world_size, use_cuda)

    if use_cuda:
        torch.cuda.set_device(rank)
        device = torch.device("cuda", rank)
    else:
        device = torch.device("cpu")

    seed = 1337 + rank
    random.seed(seed)
    torch.manual_seed(seed)

    dataset = SyntheticGraphDataset(cfg)
    sampler = DistributedSampler(dataset, num_replicas=world_size, rank=rank, shuffle=True, drop_last=False)
    loader = DataLoader(dataset, batch_size=cfg.batch_size, sampler=sampler)

    model = GraphConvNetwork(cfg.dim_in, cfg.dim_h, cfg.dim_out, cfg.num_layers).to(device)
    if use_cuda:
        model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[rank])
    else:
        model = torch.nn.parallel.DistributedDataParallel(model)

    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    model.train()
    sampler.set_epoch(0)
    for data in loader:
        data = data.to(device)
        optimizer.zero_grad(set_to_none=True)
        _, out = model(data.x, data.edge_index, data.edge_attr, data.batch)
        loss = F.binary_cross_entropy(out.view(-1), data.y.view(-1))
        loss.backward()
        optimizer.step()
        print(f"rank={rank} loss={float(loss):.6f}")
        break

    dist.barrier()
    dist.destroy_process_group()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--world-size", type=int, default=2)
    parser.add_argument("--force-cpu", action="store_true")
    args = parser.parse_args()

    cfg = Config(world_size=args.world_size, force_cpu=args.force_cpu)
    os.environ.setdefault("MASTER_ADDR", "127.0.0.1")
    os.environ.setdefault("MASTER_PORT", str(29500 + (os.getpid() % 1000)))
    print(f"torch={torch.__version__}")
    print(f"cuda_available={torch.cuda.is_available()}")
    print(f"cuda_device_count={torch.cuda.device_count()}")
    print(f"world_size={cfg.world_size}")
    print(f"force_cpu={cfg.force_cpu}")
    print("starting distributed repro")
    mp.spawn(run_worker, args=(cfg.world_size, cfg), nprocs=cfg.world_size, join=True)
    print("completed without segfault")


if __name__ == "__main__":
    main()
