import traceback

import torch
from peft import LoraConfig, get_peft_model
from transformers import LlamaConfig, LlamaForCausalLM


def _build_model() -> torch.nn.Module:
    config = LlamaConfig(
        hidden_size=16,
        intermediate_size=32,
        num_hidden_layers=2,
        num_attention_heads=4,
        num_key_value_heads=2,
        vocab_size=128,
        max_position_embeddings=64,
        pad_token_id=0,
    )
    base_model = LlamaForCausalLM(config)
    peft_config = LoraConfig(
        r=8,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],
        task_type="CAUSAL_LM",
    )
    return get_peft_model(base_model, peft_config)


def main() -> int:
    import deepspeed

    deepspeed.init_distributed(dist_backend="gloo", dist_init_required=True)
    import deepspeed.comm as dist

    rank = dist.get_rank()
    world_size = dist.get_world_size()
    if rank == 0:
        print(f"world_size={world_size}")

    # Keep the repro local and deterministic.
    torch.manual_seed(0)

    model = _build_model()
    if rank == 0:
        print(f"model_type={type(model).__name__}")

    from deepspeed.runtime.sequence_parallel.ulysses_sp import UlyssesSPAttentionHF

    try:
        UlyssesSPAttentionHF.register_with_transformers(
            model_name_or_path=model,
            core_attn_implementation="sdpa",
            sequence_parallel_size=2,
            micro_batch_size=1,
            seq_length=64,
            seq_length_is_variable=True,
        )
    except Exception as exc:
        if rank == 0:
            print(f"exception_type={type(exc).__name__}")
            print(f"exception_message={exc}")
            traceback.print_exc()
        return 0
    else:
        if rank == 0:
            print("unexpected_success")
        return 1
    finally:
        if dist.is_initialized():
            dist.destroy_process_group()


if __name__ == "__main__":
    raise SystemExit(main())
