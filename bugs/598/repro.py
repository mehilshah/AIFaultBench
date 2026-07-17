#!/usr/bin/env python3
import tempfile

import torch
import torch.nn as nn

from accelerate import dispatch_model


class ToyLM(nn.Module):
    def __init__(self):
        super().__init__()
        self.embed_tokens = nn.Embedding(8, 4)
        self.lm_head = nn.Linear(4, 8, bias=False)
        self.tie_weights()

    def tie_weights(self):
        self.lm_head.weight = self.embed_tokens.weight


def main():
    model = ToyLM()
    print("pre_dispatch_shared:", model.embed_tokens.weight is model.lm_head.weight)
    print(
        "pre_dispatch_named_parameters:",
        [name for name, _ in model.named_parameters()],
    )

    with tempfile.TemporaryDirectory() as offload_dir:
        device_map = {"embed_tokens": "disk", "lm_head": "cpu"}
        model = dispatch_model(model, device_map=device_map, offload_dir=offload_dir)

        post_dispatch_shared = model.embed_tokens.weight is model.lm_head.weight
        post_dispatch_names = [name for name, _ in model.named_parameters()]
        print("post_dispatch_shared:", post_dispatch_shared)
        print("post_dispatch_embed_device:", model.embed_tokens.weight.device)
        print("post_dispatch_lm_head_device:", model.lm_head.weight.device)
        print("post_dispatch_named_parameters:", post_dispatch_names)

        model.tie_weights()
        print("after_retie_shared:", model.embed_tokens.weight is model.lm_head.weight)
        print(
            "after_retie_named_parameters:",
            [name for name, _ in model.named_parameters()],
        )

        if (not post_dispatch_shared) or ("lm_head.weight" in post_dispatch_names):
            raise AssertionError(
                "dispatch_model broke the tied weight relationship between embed_tokens and lm_head"
            )

    print("repro_status: not reproduced")


if __name__ == "__main__":
    main()
