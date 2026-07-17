#!/usr/bin/env python3
import json
import os
import random
import socket

import torch

import deepspeed


def find_free_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


class SimpleModel(torch.nn.Module):
    def __init__(self, hidden_dim):
        super().__init__()
        self.linear = torch.nn.Linear(hidden_dim, hidden_dim)
        self.loss_fn = torch.nn.CrossEntropyLoss()

    def forward(self, x, y):
        logits = self.linear(x)
        return self.loss_fn(logits, y)


def grad_norm(module):
    norms = []
    for param in module.parameters():
        if param.grad is not None:
            norms.append(param.grad.detach().float().norm())
    if not norms:
        return 0.0
    return torch.linalg.vector_norm(torch.stack(norms)).item()


def non_none_grads(module):
    return sum(1 for param in module.parameters() if param.grad is not None)


def run_stage(zero_stage):
    torch.manual_seed(1234)
    random.seed(1234)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(1234)

    torch.cuda.set_device(0)
    if torch.distributed.is_initialized():
        torch.distributed.destroy_process_group()

    os.environ.setdefault("RANK", "0")
    os.environ.setdefault("WORLD_SIZE", "1")
    os.environ.setdefault("LOCAL_RANK", "0")
    os.environ.setdefault("MASTER_ADDR", "127.0.0.1")
    os.environ["MASTER_PORT"] = os.environ.get("MASTER_PORT", str(find_free_port()))

    torch.distributed.init_process_group(backend="nccl", rank=0, world_size=1)

    hidden_dim = 16
    batch_size = 8

    model = SimpleModel(hidden_dim)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.0)
    config = {
        "train_batch_size": batch_size,
        "train_micro_batch_size_per_gpu": batch_size,
        "gradient_accumulation_steps": 1,
        "bf16": {
            "enabled": True
        },
        "zero_optimization": {
            "stage": zero_stage,
        },
        "steps_per_print": 1,
    }

    engine, _, _, _ = deepspeed.initialize(
        config=config,
        model=model,
        model_parameters=list(model.parameters()),
        optimizer=optimizer,
        dist_init_required=False,
    )

    x = torch.randn(batch_size, hidden_dim, device=engine.device, dtype=torch.bfloat16)
    y = torch.randint(0, hidden_dim, (batch_size,), device=engine.device, dtype=torch.long)

    norms = []
    post_step_grads = []
    for step_idx in range(3):
        loss = engine(x, y)
        engine.backward(loss)
        norms.append(grad_norm(engine.module))
        engine.step()
        post_step_grads.append(non_none_grads(engine.module))
        print(
            f"stage={zero_stage} step={step_idx + 1} grad_norm={norms[-1]:.6f} "
            f"post_step_non_none_grads={post_step_grads[-1]}"
        )

    torch.distributed.destroy_process_group()
    return norms, post_step_grads


def main():
    if not torch.cuda.is_available():
        raise SystemExit("Blocking reason: CUDA GPU is required for bf16 ZeRO-0 reproduction.")

    if not torch.cuda.is_bf16_supported():
        raise SystemExit("Blocking reason: this GPU/runtime does not report bf16 support.")

    stage_env = os.environ.get("ZERO_STAGE")
    if stage_env is not None:
        zero_stage = int(stage_env)
        norms, post = run_stage(zero_stage)
        growth_ratio = norms[2] / max(norms[0], 1e-12)
        summary = {
            "zero_stage": zero_stage,
            "norms": norms,
            "post_step_non_none_grads": post,
            "growth_ratio": growth_ratio,
        }
        print(json.dumps(summary))

        if zero_stage == 0:
            if not (growth_ratio > 1.5 and post[-1] > 0):
                raise SystemExit("Stage 0 did not reproduce the gradient accumulation bug.")
        elif zero_stage == 1:
            if not (growth_ratio < 1.25 and post[-1] == 0):
                raise SystemExit("Stage 1 baseline did not clear gradients as expected.")
        else:
            raise SystemExit(f"Unsupported zero stage: {zero_stage}")
        return

    raise SystemExit("Set ZERO_STAGE=0 or ZERO_STAGE=1.")


if __name__ == "__main__":
    main()
