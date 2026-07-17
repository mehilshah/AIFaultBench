import traceback

import torch
from accelerate import Accelerator, DistributedDataParallelKwargs
from accelerate.utils import FullyShardedDataParallelPlugin
from transformers import BloomConfig, BloomForSequenceClassification, set_seed

from peft import PromptEncoderConfig, get_peft_model
from peft.utils.other import fsdp_auto_wrap_policy


def build_model():
    config = BloomConfig(
        vocab_size=128,
        hidden_size=32,
        n_layer=2,
        n_head=4,
        intermediate_size=64,
        pad_token_id=0,
        num_labels=2,
    )
    return BloomForSequenceClassification(config)


def main():
    set_seed(0)
    ddp_scaler = DistributedDataParallelKwargs(find_unused_parameters=True)
    fsdp_plugin = FullyShardedDataParallelPlugin(
        cpu_offload=True,
    )
    accelerator = Accelerator(kwargs_handlers=[ddp_scaler], fsdp_plugin=fsdp_plugin)

    model = build_model()
    model = model.to(accelerator.device)
    peft_config = PromptEncoderConfig(
        task_type="SEQ_CLS",
        num_virtual_tokens=4,
        encoder_hidden_size=16,
    )
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    if getattr(accelerator.state, "fsdp_plugin", None) is not None:
        accelerator.state.fsdp_plugin.auto_wrap_policy = fsdp_auto_wrap_policy(model)
        model = accelerator.prepare(model)

    batch = {
        "input_ids": torch.tensor([[1, 2, 3, 4], [4, 3, 2, 1]], dtype=torch.long, device=accelerator.device),
        "attention_mask": torch.tensor([[1, 1, 1, 1], [1, 1, 1, 0]], dtype=torch.long, device=accelerator.device),
        "labels": torch.tensor([0, 1], dtype=torch.long, device=accelerator.device),
    }

    print(f"accelerator.device={accelerator.device}")
    print(f"input_ids.device={batch['input_ids'].device}")
    print(f"attention_mask.device={batch['attention_mask'].device}")

    try:
        outputs = model(**batch)
        print(f"forward_ok loss={outputs.loss.item():.6f}")
    except Exception as exc:
        print("forward_failed")
        traceback.print_exc()
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
