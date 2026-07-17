from __future__ import annotations

import json
from pathlib import Path

import torch
from diffusers.models.unets.unet_2d_condition import UNet2DConditionModel


class IPAdapterWrapper(torch.nn.Module):
    def __init__(self, module: torch.nn.Module):
        super().__init__()
        self.module = module
        self.calls = 0

    def forward(self, attn, hidden_states, encoder_hidden_states=None, attention_mask=None, **kwargs):
        self.calls += 1
        return self.module(
            attn,
            hidden_states,
            encoder_hidden_states=encoder_hidden_states,
            attention_mask=attention_mask,
            **kwargs,
        )


def build_model() -> UNet2DConditionModel:
    return UNet2DConditionModel(
        block_out_channels=(4, 8),
        norm_num_groups=4,
        down_block_types=("CrossAttnDownBlock2D", "DownBlock2D"),
        up_block_types=("UpBlock2D", "CrossAttnUpBlock2D"),
        cross_attention_dim=8,
        attention_head_dim=2,
        out_channels=4,
        in_channels=4,
        layers_per_block=1,
        sample_size=16,
    ).eval()


def main() -> None:
    torch.manual_seed(0)
    model = build_model()

    processors = {}
    for name, proc in model.attn_processors.items():
        processors[name] = IPAdapterWrapper(proc) if "attn2" in name else proc
    model.set_attn_processor(processors)

    before = {name: type(proc).__name__ for name, proc in model.attn_processors.items()}
    before_attn2 = {name: type(proc).__name__ for name, proc in model.attn_processors.items() if "attn2" in name}

    sample = torch.randn(4, 4, 16, 16)
    timestep = torch.tensor([10])
    encoder_hidden_states = torch.randn(4, 4, 8)

    with torch.no_grad():
        output = model(sample, timestep, encoder_hidden_states).sample

    after = {name: type(proc).__name__ for name, proc in model.attn_processors.items()}
    after_attn2 = {name: type(proc).__name__ for name, proc in model.attn_processors.items() if "attn2" in name}

    wrapper_calls = sum(
        getattr(proc, "calls", 0) for proc in model.attn_processors.values() if hasattr(proc, "calls")
    )
    module_attn2 = type(model.down_blocks[0].attentions[0].transformer_blocks[0].attn2.processor).__name__

    print(json.dumps({"before_attn2": before_attn2, "after_attn2": after_attn2, "module_attn2": module_attn2}))
    print(f"output_shape={tuple(output.shape)}")
    print(f"wrapper_calls={wrapper_calls}")

    if before != after:
        raise AssertionError("Attention processor mapping changed across the forward pass.")
    if before_attn2 != after_attn2:
        raise AssertionError("attn2 processor types changed across the forward pass.")
    if wrapper_calls == 0:
        raise AssertionError("The custom wrapper was never invoked.")


if __name__ == "__main__":
    main()
