from __future__ import annotations

import time

import numpy as np
import torch
from torch_cluster import graclus_cluster


def run_cpu(edge_index: np.ndarray, edge_attr: np.ndarray) -> None:
    row = torch.tensor(edge_index[0], dtype=torch.long)
    col = torch.tensor(edge_index[1], dtype=torch.long)
    weight = torch.tensor(edge_attr, dtype=torch.float)

    start = time.time()
    out = graclus_cluster(row, col, weight, None)
    elapsed = time.time() - start
    print(
        f"cpu_done shape={tuple(out.shape)} first10={out[:10].tolist()} "
        f"elapsed={elapsed:.3f}s",
        flush=True,
    )


def run_gpu(edge_index: np.ndarray, edge_attr: np.ndarray) -> None:
    if not torch.cuda.is_available():
        print("cuda_unavailable", flush=True)
        return

    row = torch.tensor(edge_index[0], dtype=torch.long, device="cuda")
    col = torch.tensor(edge_index[1], dtype=torch.long, device="cuda")
    weight = torch.tensor(edge_attr, dtype=torch.float, device="cuda")

    print(
        f"gpu_start shape={tuple(row.shape)} device={row.device}",
        flush=True,
    )
    start = time.time()
    out = graclus_cluster(row, col, weight, None)
    elapsed = time.time() - start
    print(
        f"gpu_done shape={tuple(out.shape)} first10={out[:10].tolist()} "
        f"elapsed={elapsed:.3f}s",
        flush=True,
    )


def main() -> None:
    edge_index = np.loadtxt("batch_edge_index.txt", dtype=np.int64)
    edge_attr = np.loadtxt("batch_edge_attr.txt", dtype=np.float32)
    print(
        f"loaded edge_index_shape={edge_index.shape} "
        f"edge_attr_shape={edge_attr.shape}",
        flush=True,
    )
    run_cpu(edge_index, edge_attr)
    run_gpu(edge_index, edge_attr)


if __name__ == "__main__":
    main()
