#!/usr/bin/env python3
from __future__ import annotations

import os
import socket
import traceback


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def _worker(rank: int, world_size: int, master_port: int) -> None:
    os.environ["MASTER_ADDR"] = "127.0.0.1"
    os.environ["MASTER_PORT"] = str(master_port)
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"

    import torch

    torch.distributed.init_process_group("gloo", rank=rank, world_size=world_size)

    try:
        import deepspeed.comm as ds_dist
        from peft import LoraConfig, get_peft_model
        from transformers import LlamaConfig, LlamaForCausalLM, PreTrainedModel

        from deepspeed.runtime.sequence_parallel.ulysses_sp import UlyssesSPAttentionHF

        # Bind DeepSpeed's comm wrapper to the already initialized torch process group.
        ds_dist.init_distributed(dist_backend="gloo", dist_init_required=False)

        # Tiny local model so the repro runs fully offline.
        config = LlamaConfig(
            vocab_size=128,
            hidden_size=64,
            intermediate_size=128,
            num_hidden_layers=2,
            num_attention_heads=4,
            num_key_value_heads=4,
            max_position_embeddings=32,
        )
        model = LlamaForCausalLM(config)
        model = get_peft_model(
            model,
            LoraConfig(
                task_type="CAUSAL_LM",
                r=4,
                lora_alpha=8,
                lora_dropout=0.0,
            ),
        )

        if rank == 0:
            print(f"model_type={type(model).__name__}")
            print(f"isinstance_pretrained={isinstance(model, PreTrainedModel)}")

        # This should accept PEFT wrappers but currently falls through to AutoConfig.from_pretrained(...).
        UlyssesSPAttentionHF.register_with_transformers(
            model_name_or_path=model,
            core_attn_implementation="sdpa",
            sequence_parallel_size=world_size,
            micro_batch_size=1,
            seq_length=8,
            seq_length_is_variable=True,
        )

        if rank == 0:
            print("unexpected_success")
    except Exception as exc:
        print(f"[rank {rank}] {type(exc).__name__}: {exc}")
        traceback.print_exc()
        raise
    finally:
        torch.distributed.destroy_process_group()


def main() -> None:
    import torch.multiprocessing as mp

    world_size = 2
    port = _find_free_port()
    mp.set_start_method("spawn", force=True)
    mp.spawn(_worker, args=(world_size, port), nprocs=world_size, join=True)


if __name__ == "__main__":
    main()
