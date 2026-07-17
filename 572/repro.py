#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CODEBASE_SRC = ROOT / "codebase" / "src"
if str(CODEBASE_SRC) not in sys.path:
    sys.path.insert(0, str(CODEBASE_SRC))


def _require_two_gpus():
    try:
        import torch
    except Exception as exc:  # pragma: no cover - environment specific
        raise RuntimeError(f"Unable to import torch in this environment: {exc}") from exc

    gpu_count = torch.cuda.device_count() if torch.cuda.is_available() else 0
    if gpu_count < 2:
        raise RuntimeError(
            f"This reproducer needs at least 2 visible CUDA devices, but only {gpu_count} are available."
        )


def _build_dataset():
    import torch
    from torch.nn.utils.rnn import pad_sequence

    # Two batches with different sequence lengths, matching the shape-changing
    # pattern described in the bug report.
    sequences = [
        torch.tensor([10, 11, 12, 13, 14], dtype=torch.long),
        torch.tensor([10, 11, 12, 13, 14, 15, 16], dtype=torch.long),
        torch.tensor([10, 11, 12, 13], dtype=torch.long),
        torch.tensor([10, 11, 12, 13, 14, 15], dtype=torch.long),
        torch.tensor([10, 11, 12], dtype=torch.long),
        torch.tensor([10, 11, 12, 13, 14, 15, 16, 17], dtype=torch.long),
    ]
    note_ids = [torch.tensor([idx], dtype=torch.long) for idx in range(len(sequences))]

    class Dataset(torch.utils.data.Dataset):
        def __len__(self):
            return len(sequences)

        def __getitem__(self, idx):
            return sequences[idx], note_ids[idx]

    def collate(batch):
        inputs, notes = zip(*batch)
        return pad_sequence(inputs, batch_first=True, padding_value=0), torch.cat(notes, dim=0)

    return Dataset(), collate


def main():
    _require_two_gpus()

    import torch
    from accelerate import Accelerator
    from accelerate.utils.dataclasses import DeepSpeedPlugin
    from torch.utils.data import DataLoader
    from transformers import GPT2Config, GPT2LMHeadModel

    torch.manual_seed(0)

    ds_plugin = DeepSpeedPlugin(
        gradient_accumulation_steps=1,
        gradient_clipping=1.0,
        zero_stage=3,
        offload_optimizer_device="cpu",
        offload_param_device="cpu",
        zero3_init_flag=True,
    )

    accelerator = Accelerator(mixed_precision="bf16", deepspeed_plugin=ds_plugin)
    dataset, collate = _build_dataset()
    dataloader = DataLoader(dataset, shuffle=False, batch_size=2, collate_fn=collate)
    chunk_dataloader = DataLoader(dataset, shuffle=False, batch_size=2, collate_fn=collate)

    config = GPT2Config(
        vocab_size=64,
        n_positions=32,
        n_ctx=32,
        n_embd=32,
        n_layer=2,
        n_head=4,
        bos_token_id=1,
        eos_token_id=2,
        pad_token_id=0,
    )
    model = GPT2LMHeadModel(config)
    model.eval()

    model, dataloader, chunk_dataloader = accelerator.prepare(model, dataloader, chunk_dataloader)

    for step, (data, note_idx) in enumerate(zip(dataloader, chunk_dataloader), start=1):
        start = time.perf_counter()
        outputs = model.generate(data, max_new_tokens=5)
        outputs = accelerator.gather(outputs)
        note_idx = accelerator.gather(note_idx)
        elapsed = time.perf_counter() - start
        if accelerator.is_local_main_process:
            print(
                json.dumps(
                    {
                        "step": step,
                        "elapsed_sec": round(elapsed, 3),
                        "input_shape": list(data.shape),
                        "output_shape": list(outputs.shape),
                        "note_idx_shape": list(note_idx.shape),
                    }
                )
            )


if __name__ == "__main__":
    main()
