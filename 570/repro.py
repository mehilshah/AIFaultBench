#!/usr/bin/env python3
"""Reproduce the QwenImage Ulysses context-parallel mask mismatch.

The reported bug shows that SP-enabled and non-SP outputs diverge when
`encoder_hidden_states_mask` contains a non-contiguous pattern.

This script runs the same comparison in a small local distributed setup.
It defaults to CPU/gloo when CUDA is unavailable, which still reproduces
the mismatch in this workspace.
"""

from __future__ import annotations

import json
import os
import socket
from datetime import timedelta

import torch
import torch.distributed as dist
import torch.multiprocessing as mp
from torch.distributed.device_mesh import init_device_mesh

from diffusers import ContextParallelConfig, QwenImageTransformer2DModel


SP_SIZE = 2
MODEL_CONFIG = {
    "patch_size": 2,
    "in_channels": 16,
    "out_channels": 4,
    "num_layers": 2,
    "attention_head_dim": 16,
    "num_attention_heads": 4,
    "joint_attention_dim": 16,
    "guidance_embeds": False,
    "axes_dims_rope": (8, 4, 4),
}


def _find_free_port() -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 0))
    sock.listen(1)
    port = sock.getsockname()[1]
    sock.close()
    return port


def _worker(rank: int, world_size: int, port: int) -> None:
    os.environ["MASTER_ADDR"] = "127.0.0.1"
    os.environ["MASTER_PORT"] = str(port)
    os.environ["RANK"] = str(rank)
    os.environ["WORLD_SIZE"] = str(world_size)

    backend = "nccl" if torch.cuda.is_available() else "gloo"
    dist.init_process_group(backend=backend, timeout=timedelta(seconds=3600))

    if torch.cuda.is_available():
        torch.cuda.set_device(rank)
        device = torch.device(f"cuda:{rank}")
        dtype = torch.bfloat16
    else:
        device = torch.device("cpu")
        dtype = torch.float32

    mesh = init_device_mesh(
        device.type,
        mesh_shape=(1, 1, SP_SIZE),
        mesh_dim_names=("dp", "ring", "ulysses"),
    )

    module_sp = QwenImageTransformer2DModel(**MODEL_CONFIG)
    module_sp.enable_parallelism(config=ContextParallelConfig(ulysses_degree=SP_SIZE, mesh=mesh))
    module_sp = module_sp.to(device, dtype=dtype)
    for param in module_sp.parameters():
        dist.broadcast(param.data, src=0)

    module_no_sp = QwenImageTransformer2DModel(**MODEL_CONFIG).to(device, dtype=dtype)
    module_no_sp.load_state_dict({k: v.clone() for k, v in module_sp.state_dict().items()}, strict=False)

    batch_size, latent_h, text_seq_len = 2, 4, 8
    latent_dim, text_dim = MODEL_CONFIG["in_channels"], MODEL_CONFIG["joint_attention_dim"]

    hidden_states = torch.zeros(batch_size, latent_h * latent_h, latent_dim, dtype=dtype, device=device)
    encoder_hidden_states = torch.zeros(batch_size, text_seq_len, text_dim, dtype=dtype, device=device)
    if rank == 0:
        torch.manual_seed(42)
        hidden_states.normal_()
        encoder_hidden_states.normal_()
    dist.broadcast(hidden_states, src=0)
    dist.broadcast(encoder_hidden_states, src=0)

    encoder_hidden_states_mask = torch.zeros(batch_size, text_seq_len, dtype=torch.bool, device=device)
    encoder_hidden_states_mask[0, :2] = True
    encoder_hidden_states_mask[1, :6] = True

    model_inputs = {
        "hidden_states": hidden_states,
        "timestep": torch.full([batch_size], 0.5, dtype=torch.float32, device=device),
        "encoder_hidden_states": encoder_hidden_states,
        "encoder_hidden_states_mask": encoder_hidden_states_mask,
        "img_shapes": [[(1, latent_h, latent_h)]] * batch_size,
        "return_dict": False,
    }

    module_sp.eval()
    module_no_sp.eval()
    with torch.no_grad():
        output_sp = module_sp(**model_inputs)[0]
        output_no_sp = module_no_sp(**model_inputs)[0]

    if rank == 0:
        diff = (output_sp.float() - output_no_sp.float()).abs()
        summary = {
            "device": str(device),
            "backend": backend,
            "sp_size": SP_SIZE,
            "output_shape": list(output_sp.shape),
            "mean_sp": output_sp.float().mean().item(),
            "mean_no_sp": output_no_sp.float().mean().item(),
            "max_abs_diff": diff.max().item(),
            "mismatched_elements": int(
                (~torch.isclose(output_sp.float(), output_no_sp.float(), rtol=1e-2, atol=1e-2)).sum().item()
            ),
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
        torch.testing.assert_close(output_sp.float(), output_no_sp.float(), rtol=1e-2, atol=1e-2)

    dist.destroy_process_group()


def main() -> None:
    port = _find_free_port()
    mp.spawn(_worker, args=(SP_SIZE, port), nprocs=SP_SIZE, join=True)


if __name__ == "__main__":
    main()
