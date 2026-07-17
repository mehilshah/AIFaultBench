import argparse
import gc
import os
import shutil
import tempfile

import psutil
import torch
from torch_geometric.data import Data, Dataset
from torch_geometric.loader import DataLoader


class CustomDataset(Dataset):
    def __init__(self, root, num_graphs=150):
        self.num_graphs = num_graphs
        self.data_dir = os.path.join(root, 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        super().__init__(root)

    def len(self):
        return self.num_graphs

    def get(self, idx):
        path = os.path.join(self.data_dir, f'{idx}.pt')
        if os.path.exists(path):
            return torch.load(path, weights_only=False)

        x = torch.randn((500, 1024))
        edge_index = torch.randint(0, 500, (2, 1500))
        y = torch.tensor([idx % 2], dtype=torch.long)
        data = Data(x=x, edge_index=edge_index, y=y)
        torch.save(data, path)
        return data


def rss_mb():
    return psutil.Process().memory_info().rss / 1024**2


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', type=int, default=30)
    parser.add_argument('--num-graphs', type=int, default=150)
    return parser.parse_args()


def main():
    args = parse_args()
    root = tempfile.mkdtemp(prefix='pyg_bug_')
    try:
        dataset = CustomDataset(root=root, num_graphs=args.num_graphs)
        loader = DataLoader(dataset, batch_size=16, shuffle=True, num_workers=0)

        print(f'PyTorch: {torch.__version__}')
        print(f'PyG: {__import__("torch_geometric").__version__}')
        print(f'before {rss_mb():.2f} MB', flush=True)

        for epoch in range(args.epochs):
            for _ in loader:
                pass
            gc.collect()
            print(f'epoch {epoch} {rss_mb():.2f} MB', flush=True)
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == '__main__':
    main()
