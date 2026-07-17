#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import torch
from torch import nn


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
sys.path.insert(0, str(CODEBASE))

from tensordict.nn import TensorDictModule  # noqa: E402
from torchrl.data import Bounded  # noqa: E402
from torchrl.modules import ProbabilisticActor  # noqa: E402
from torchrl.modules.distributions import NormalParamExtractor  # noqa: E402
from torchrl.modules.distributions.continuous import TanhNormal  # noqa: E402
from torchrl.modules.tensordict_module import ValueOperator  # noqa: E402
from torchrl.objectives import CrossQLoss  # noqa: E402


def build_actor(obs_dim: int, action_dim: int) -> ProbabilisticActor:
    action_spec = Bounded(
        -torch.ones(action_dim), torch.ones(action_dim), (action_dim,)
    )
    net = nn.Sequential(nn.Linear(obs_dim, 2 * action_dim), NormalParamExtractor())
    module = TensorDictModule(
        net,
        in_keys=["observation"],
        out_keys=["loc", "scale"],
    )
    return ProbabilisticActor(
        module=module,
        in_keys=["loc", "scale"],
        spec=action_spec,
        distribution_class=TanhNormal,
        out_keys=["action"],
    )


class ValueClass(nn.Module):
    def __init__(self, obs_dim: int, action_dim: int) -> None:
        super().__init__()
        self.linear = nn.Linear(obs_dim + action_dim, 1)

    def forward(self, obs, act):
        return self.linear(torch.cat([obs, act], -1))


def main() -> None:
    obs_dim = 3
    action_dim = 4

    actor = build_actor(obs_dim, action_dim)
    qvalue = ValueOperator(
        module=ValueClass(obs_dim, action_dim),
        in_keys=["observation", "action"],
    )

    print("Creating CrossQLoss with a numeric target_entropy...")
    CrossQLoss(
        actor_network=actor,
        qvalue_network=qvalue,
        target_entropy=-action_dim,
    )
    print("Unexpected success: the bug did not reproduce.")


if __name__ == "__main__":
    main()
