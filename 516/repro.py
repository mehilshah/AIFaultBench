#!/usr/bin/env python3
from __future__ import annotations

import torch
from torch import nn
from torchrl.modules.models.multiagent import MultiAgentNetBase


class SingleAgentMLP(nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim, seq_len):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, out_dim),
        )

    def forward(self, x):
        return self.net(x)


class MultiAgentPolicyNet(MultiAgentNetBase):
    def __init__(
        self,
        single_net,
        obs_dim,
        sequence_length,
        action_dim,
        n_agents,
        share_params=True,
        centralized=False,
        device=None,
    ):
        self.obs_dim = obs_dim
        self.action_dim = action_dim
        self.single_net = single_net
        self.seq_len = sequence_length
        super().__init__(
            n_agents=n_agents,
            centralized=centralized,
            share_params=share_params,
            agent_dim=-2,
            device=device,
        )

    def _build_single_net(self, *, device, **kwargs):
        net = self.single_net(
            self.obs_dim,
            self.obs_dim,
            self.action_dim,
            self.seq_len,
        )
        return net.to(device) if device is not None else net

    def _pre_forward_check(self, inputs):
        return inputs


def main() -> None:
    torch.manual_seed(0)
    net = MultiAgentPolicyNet(
        SingleAgentMLP,
        obs_dim=2,
        sequence_length=1,
        action_dim=4,
        n_agents=3,
        share_params=True,
        centralized=True,
    )
    x = torch.randn(4, 3, 2)
    y = net(x)
    print(f"input_shape={tuple(x.shape)}")
    print(f"output_shape={tuple(y.shape)}")
    expected_shape = (4, 3, 4)
    assert tuple(y.shape) == expected_shape, (
        f"Expected output shape {expected_shape}, got {tuple(y.shape)}"
    )


if __name__ == "__main__":
    main()
