#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

import torch
from safetensors.torch import save_file
from transformers import GPT2Config, GPT2LMHeadModel


ROOT = Path(__file__).resolve().parent
CODEBASE_SRC = ROOT / "codebase" / "src"
if str(CODEBASE_SRC) not in sys.path:
    sys.path.insert(0, str(CODEBASE_SRC))

from accelerate import Accelerator  # noqa: E402


def main() -> None:
    accelerator = Accelerator()
    print(f"distributed_type={accelerator.distributed_type}", flush=True)
    print(f"device={accelerator.device}", flush=True)
    print(f"fsdp_version={getattr(accelerator.state.fsdp_plugin, 'fsdp_version', None)}", flush=True)

    config = GPT2Config(
        n_layer=1,
        n_head=1,
        n_embd=8,
        n_positions=8,
        vocab_size=16,
        n_inner=16,
    )
    model = GPT2LMHeadModel(config)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    model, optimizer = accelerator.prepare(model, optimizer)

    input_ids = torch.randint(0, config.vocab_size, (1, 4), device=accelerator.device)
    labels = torch.randint(0, config.vocab_size, (1, 4), device=accelerator.device)
    loss = model(input_ids=input_ids, labels=labels).loss
    accelerator.backward(loss)
    optimizer.step()
    optimizer.zero_grad()

    unwrapped = accelerator.unwrap_model(model)
    print(f"unwrapped_type={type(unwrapped).__name__}", flush=True)
    print(f"has_module={hasattr(unwrapped, 'module')}", flush=True)

    state_dict = unwrapped.state_dict()
    sample_types = {name: type(tensor).__name__ for name, tensor in list(state_dict.items())[:3]}
    print(f"state_dict_sample_types={sample_types}", flush=True)

    output_dir = Path(tempfile.mkdtemp(prefix="fsdp2_dtensor_repro_"))
    output_path = output_dir / "model.safetensors"
    print(f"save_file_target={output_path}", flush=True)

    # This is the failing path from the bug report: DTensor-backed weights reach safetensors.
    save_file(state_dict, str(output_path))


if __name__ == "__main__":
    main()
