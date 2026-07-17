from __future__ import annotations

import torch

import transformers.masking_utils as masking_utils
import transformers.models.qwen3.modeling_qwen3 as modeling_qwen3
from transformers import Qwen3Config
from transformers.masking_utils import create_masks_for_generate
from transformers.models.qwen3.modeling_qwen3 import Qwen3Model


def main() -> None:
    calls: list[object | None] = []

    def fake_create_causal_mask(*args, **kwargs):
        calls.append(kwargs.get("attention_mask"))
        return None

    # Patch both call sites: create_masks_for_generate resolves from the mask
    # registry, while Qwen3Model.forward uses the module-level import.
    masking_utils.LAYER_PATTERN_TO_MASK_FUNCTION_MAPPING["full_attention"] = fake_create_causal_mask
    modeling_qwen3.create_causal_mask = fake_create_causal_mask

    config = Qwen3Config(
        vocab_size=32,
        hidden_size=16,
        intermediate_size=32,
        num_hidden_layers=1,
        num_attention_heads=4,
        num_key_value_heads=4,
        head_dim=4,
        max_position_embeddings=32,
        sliding_window=None,
        layer_types=["full_attention"],
        pad_token_id=0,
    )
    model = Qwen3Model(config)

    input_ids = torch.tensor([[1, 2, 3]], dtype=torch.long)
    embeds = model.embed_tokens(input_ids)

    attention_mask = create_masks_for_generate(
        config,
        embeds,
        attention_mask=None,
        past_key_values=None,
        position_ids=None,
    )

    print(f"create_masks_for_generate_return_type={type(attention_mask).__name__}")
    print(f"create_masks_for_generate_return_value={attention_mask}")
    print(f"causal_mask_calls_after_precompute={len(calls)}")

    output = model(input_ids=input_ids, attention_mask=attention_mask, use_cache=False)
    print(f"forward_output_shape={tuple(output.last_hidden_state.shape)}")
    print(f"causal_mask_calls_after_forward={len(calls)}")
    print(f"causal_mask_call_history={calls}")

    assert isinstance(attention_mask, dict), (
        "Bug reproduced: create_masks_for_generate returned a bare mask instead of "
        "a dict for Qwen3 layer_types=['full_attention']"
    )
    assert len(calls) == 1, (
        "Bug reproduced: Qwen3Model.forward called create_causal_mask again after "
        "receiving a precomputed mask"
    )


if __name__ == "__main__":
    main()

