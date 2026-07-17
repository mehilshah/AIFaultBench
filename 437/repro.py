import math
import os
from pathlib import Path
from tempfile import TemporaryDirectory

import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from accelerate import Accelerator


def _collect_wandb_warnings(wandb_root: Path) -> list[str]:
    warnings = []
    for path in wandb_root.glob("wandb/**/logs/debug*.log"):
        try:
            text = path.read_text(errors="ignore")
        except OSError:
            continue
        for line in text.splitlines():
            if "Dropping entry" in line or "monotonically increasing" in line:
                warnings.append(line.strip())
    return warnings


def main() -> None:
    with TemporaryDirectory(prefix="wandb-", dir=os.getcwd()) as wandb_dir:
        os.environ["WANDB_DIR"] = wandb_dir
        os.environ["WANDB_MODE"] = "offline"

        accelerator = Accelerator(log_with="wandb")
        accelerator.init_trackers("accelerate-wandb-step-regression")

        model = nn.Linear(4, 1)
        optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
        train_loader = DataLoader(TensorDataset(torch.randn(6, 4), torch.randn(6, 1)), batch_size=2)
        eval_loader = DataLoader(TensorDataset(torch.randn(6, 4), torch.randn(6, 1)), batch_size=2)

        completed_steps = 0
        completed_eval_steps = 0

        for epoch in range(1):
            model.train()
            total_loss = 0

            for _, batch in enumerate(train_loader):
                inputs, targets = batch
                with accelerator.accumulate(model):
                    outputs = model(inputs)
                    loss = ((outputs - targets) ** 2).mean()
                    total_loss += loss.detach().float()
                    accelerator.backward(loss)
                    optimizer.step()
                    optimizer.zero_grad()

                if accelerator.sync_gradients:
                    completed_steps += 1

                accelerator.log({"batch_train_loss": loss}, step=completed_steps)

            model.eval()
            losses = []
            for _, batch in enumerate(eval_loader):
                inputs, targets = batch
                with torch.no_grad():
                    outputs = model(inputs)
                loss = ((outputs - targets) ** 2).mean()
                completed_eval_steps += 1
                losses.append(accelerator.gather(loss.repeat(2)))

                accelerator.log({"batch_eval_loss": loss}, step=completed_eval_steps)

            losses = torch.cat(losses)
            eval_loss = torch.mean(losses)
            perplexity = math.exp(eval_loss)

            accelerator.log(
                {
                    "perplexity": perplexity,
                    "eval_loss": eval_loss,
                    "train_loss": total_loss.item() / len(train_loader),
                    "epoch": epoch,
                    "step": completed_steps,
                },
                step=completed_steps,
            )

        accelerator.end_training()

        wandb_root = Path(wandb_dir)
        print(f"wandb_dir={wandb_root}")
        warnings = _collect_wandb_warnings(wandb_root)
        for line in warnings:
            print(line)
        if warnings:
            print("reproduced: out-of-order eval steps were dropped by W&B")
        else:
            print("reproduction complete; inspect stderr for the W&B drop warnings")


if __name__ == "__main__":
    main()
