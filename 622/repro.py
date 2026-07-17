#!/usr/bin/env python3
"""Minimal reproduction for the ErnieImagePipeline callback locals() bug."""

from __future__ import annotations

import os
import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))

import torch  # noqa: E402
from diffusers.pipelines.ernie_image.pipeline_ernie_image import ErnieImagePipeline  # noqa: E402


class BaseDummy(torch.nn.Module):
    @property
    def device(self):
        return torch.device("cpu")


class DummyVAE(BaseDummy):
    def __init__(self):
        super().__init__()

        class Config:
            block_out_channels = ()

        self.config = Config()


class DummyTransformer(BaseDummy):
    def __init__(self):
        super().__init__()
        self.dtype = torch.float32

        class Config:
            in_channels = 4
            text_in_dim = 3

        self.config = Config()

    def forward(self, hidden_states, timestep, text_bth, text_lens, return_dict=False):
        return (torch.zeros_like(hidden_states),)


class DummyTextEncoder(BaseDummy):
    def __init__(self):
        super().__init__()
        self.dtype = torch.float32

    def forward(self, input_ids, output_hidden_states=True):
        raise RuntimeError("not used in this repro")


class DummyTokenizer:
    pass


class DummyScheduler:
    def set_timesteps(self, sigmas, device):
        self.timesteps = sigmas

    def step(self, pred, t, latents):
        return types.SimpleNamespace(prev_sample=latents)


def main():
    print(f"python={sys.version.split()[0]} torch={torch.__version__}")
    print("building dummy ErnieImagePipeline instance")
    pipe = ErnieImagePipeline(
        transformer=DummyTransformer(),
        vae=DummyVAE(),
        text_encoder=DummyTextEncoder(),
        tokenizer=DummyTokenizer(),
        scheduler=DummyScheduler(),
    )

    prompt_embeds = [torch.zeros(2, 3)]

    print("calling pipeline with callback_on_step_end_tensor_inputs=['latents']")
    pipe(
        prompt_embeds=prompt_embeds,
        output_type="latent",
        callback_on_step_end=lambda *args: {},
        callback_on_step_end_tensor_inputs=["latents"],
        use_pe=False,
        num_inference_steps=1,
        height=8,
        width=8,
        guidance_scale=1.0,
    )


if __name__ == "__main__":
    main()
