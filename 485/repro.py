from __future__ import annotations

import warnings

import torch
from lightning_fabric import Fabric
from pytorch_lightning.demos.boring_classes import BoringModel, RandomDataset
from torch.utils.data import DataLoader


def main() -> None:
    warnings.filterwarnings(message=".*AccumulateGrad.*", action="error")

    device_count = torch.cuda.device_count()
    print(f"torch={torch.__version__}")
    print(f"cuda_available={torch.cuda.is_available()}")
    print(f"cuda_device_count={device_count}")
    if torch.cuda.is_available():
        print(f"cuda_capability={torch.cuda.get_device_capability(0)}")
        print(f"cuda_arch_list={torch.cuda.get_arch_list()}")
        print(f"cuda_device_name={torch.cuda.get_device_name(0)}")

    if device_count < 1:
        raise RuntimeError("This repro needs at least one CUDA device.")

    # The original report used two GPUs. On a single-GPU host, we still force DDP
    # so the same code path is exercised as far as the local hardware allows.
    devices = 2 if device_count >= 2 else 1
    print(f"using_devices={devices}")

    batch_size = 32
    accumulation_steps = 2
    max_steps = 20

    fabric = Fabric(accelerator="gpu", strategy="ddp", devices=devices)
    fabric.launch()
    print(f"strategy={type(fabric.strategy).__name__}")

    model = BoringModel()
    optimizer = torch.optim.Adam(params=model.parameters(), lr=1e-3)
    model, optimizer = fabric.setup(model, optimizer)

    dummy_dataset = RandomDataset(size=32, length=100)
    train_loader = DataLoader(dataset=dummy_dataset, batch_size=batch_size, shuffle=True)
    train_loader = fabric.setup_dataloaders(train_loader)

    model.train()
    global_step = 0
    while global_step < max_steps:
        for batch in train_loader:
            if global_step >= max_steps:
                break

            print(f"step={global_step}")
            is_accumulating = (global_step + 1) % accumulation_steps != 0
            with fabric.no_backward_sync(model, enabled=is_accumulating):
                output = model(batch)
                loss = output.sum() / accumulation_steps
                fabric.backward(loss)

            if not is_accumulating:
                optimizer.step()
                optimizer.zero_grad()

            global_step += 1


if __name__ == "__main__":
    main()
