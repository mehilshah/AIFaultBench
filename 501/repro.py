from __future__ import annotations

import json
import os
import random
import sys
from pathlib import Path

import numpy as np
import torch
import torch.distributed as dist
import torch.nn as nn


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
if str(CODEBASE) not in sys.path:
    sys.path.insert(0, str(CODEBASE))

os.environ.setdefault("DS_ACCELERATOR", "cpu")
os.environ.setdefault("MASTER_ADDR", "127.0.0.1")
os.environ.setdefault("MASTER_PORT", "29509")
os.environ.setdefault("RANK", "0")
os.environ.setdefault("WORLD_SIZE", "1")
os.environ.setdefault("LOCAL_RANK", "0")

import deepspeed  # noqa: E402
from deepspeed.runtime.pipe.module import PipelineModule  # noqa: E402


class LoggingSGD(torch.optim.SGD):

    def __init__(self, params, lr=0.0):
        super().__init__(params, lr=lr)
        self.logged_norms = []

    def step(self, closure=None):
        total = 0.0
        for group in self.param_groups:
            for param in group["params"]:
                if param.grad is not None:
                    total += param.grad.detach().float().norm().item()
        self.logged_norms.append(total)
        return super().step(closure)


class ToyDataset(torch.utils.data.Dataset):

    def __init__(self, xs, ys):
        self.xs = xs
        self.ys = ys

    def __len__(self):
        return len(self.xs)

    def __getitem__(self, idx):
        return self.xs[idx], self.ys[idx]


def seed_all(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def make_engine(gas: int, micro_batch: int, xs: torch.Tensor, ys: torch.Tensor):
    seed_all(1234)

    model = PipelineModule(layers=[nn.Linear(4, 4, bias=False)], num_stages=1, loss_fn=nn.MSELoss())
    optimizer = LoggingSGD(model.parameters(), lr=0.0)
    config = {
        "train_batch_size": gas * micro_batch,
        "train_micro_batch_size_per_gpu": micro_batch,
        "gradient_accumulation_steps": gas,
        "steps_per_print": 1,
        "optimizer": {
            "type": "SGD",
            "params": {
                "lr": 0.0,
            },
        },
        "zero_optimization": {
            "stage": 0,
        },
        "pipeline": {
            "seed_layers": True,
        },
    }

    dataset = ToyDataset(xs, ys)
    engine, _, _, _ = deepspeed.initialize(config=config,
                                           model=model,
                                           model_parameters=model.parameters(),
                                           optimizer=optimizer,
                                           training_data=dataset)
    return engine, optimizer


def run_case(gas: int, micro_batch: int, xs: torch.Tensor, ys: torch.Tensor):
    engine, optimizer = make_engine(gas, micro_batch, xs, ys)
    loss = engine.train_batch()
    return float(loss), optimizer.logged_norms[-1]


def main() -> int:
    if not dist.is_initialized():
        deepspeed.init_distributed(dist_backend="gloo")

    xs = torch.tensor([
        [1.0, 2.0, 3.0, 4.0],
        [2.0, 0.0, 1.0, 3.0],
        [0.5, 0.5, 0.5, 0.5],
        [4.0, 3.0, 2.0, 1.0],
        [1.0, 0.0, 1.0, 0.0],
        [0.0, 1.0, 0.0, 1.0],
        [1.5, 2.5, 3.5, 4.5],
        [2.5, 3.5, 4.5, 5.5],
    ], dtype=torch.float32)
    ys = torch.tensor([
        [0.0, 1.0, 0.0, 1.0],
        [1.0, 0.0, 1.0, 0.0],
        [0.5, 1.5, 0.5, 1.5],
        [1.0, 1.0, 1.0, 1.0],
        [0.0, 0.0, 0.0, 0.0],
        [1.0, 1.0, 1.0, 1.0],
        [2.0, 2.0, 2.0, 2.0],
        [3.0, 3.0, 3.0, 3.0],
    ], dtype=torch.float32)

    gas1_loss, gas1_norm = run_case(1, 8, xs, ys)
    gas4_loss, gas4_norm = run_case(4, 2, xs, ys)
    ratio = gas4_norm / gas1_norm if gas1_norm else None

    result = {
        "gas1_loss": gas1_loss,
        "gas1_norm": gas1_norm,
        "gas4_loss": gas4_loss,
        "gas4_norm": gas4_norm,
        "ratio": ratio,
        "delta": abs(gas4_norm - gas1_norm),
    }
    print(json.dumps(result, sort_keys=True))

    if abs(gas1_norm - gas4_norm) < 1e-9 and abs(gas1_loss - gas4_loss) < 1e-9:
        print("No gradient scaling discrepancy observed.")
        return 0

    print("Gradient scaling discrepancy observed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
