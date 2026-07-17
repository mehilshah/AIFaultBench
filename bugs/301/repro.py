#!/usr/bin/env python3
from __future__ import annotations

import os
import socket
import sys
import traceback
from pathlib import Path

import torch
import torch.distributed as dist
import torch.nn as nn


ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "codebase" / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def main() -> int:
    from lightning.pytorch.strategies import FSDPStrategy

    print(f"torch={torch.__version__}")
    import lightning.pytorch as pl

    print(f"lightning={pl.__version__}")

    port = _find_free_port()
    os.environ["MASTER_ADDR"] = "127.0.0.1"
    os.environ["MASTER_PORT"] = str(port)

    dist.init_process_group("gloo", rank=0, world_size=1, init_method=f"tcp://127.0.0.1:{port}")
    print(f"distributed_initialized={dist.is_initialized()}")

    strategy = FSDPStrategy()
    strategy._parallel_devices = [torch.device("cpu")]

    class MockLightningModule(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.layer = nn.Linear(2, 2)
            self.trainer = None

    strategy._lightning_module = MockLightningModule()
    model = nn.Linear(2, 2)

    print(f"root_device={strategy.root_device}")
    print(f"root_device.index={strategy.root_device.index!r}")
    print("attempting FSDPStrategy._setup_model(model) on CPU")

    try:
        strategy._setup_model(model)
    except Exception:
        traceback.print_exc()
        return 1
    finally:
        if dist.is_initialized():
            dist.destroy_process_group()

    print("FSDPStrategy._setup_model completed without raising")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
