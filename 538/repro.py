from __future__ import annotations

import sys
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
if str(CODEBASE) not in sys.path:
    sys.path.insert(0, str(CODEBASE))

from torch import nn  # noqa: E402
from torchrl.data import BoundedContinuous  # noqa: E402
from torchrl.modules.distributions import NormalParamExtractor, TanhNormal  # noqa: E402
from torchrl.modules.tensordict_module.actors import (  # noqa: E402
    ProbabilisticActor,
    ValueOperator,
)
from torchrl.modules.tensordict_module.common import SafeModule  # noqa: E402
from torchrl.objectives.sac import SACLoss  # noqa: E402


def build_loss() -> SACLoss:
    n_act, n_obs = 2, 3
    action_spec = BoundedContinuous(
        low=-torch.ones(n_act),
        high=torch.ones(n_act),
        shape=(n_act,),
    )
    policy_net = nn.Sequential(nn.Linear(n_obs, 2 * n_act), NormalParamExtractor())
    policy_module = SafeModule(
        policy_net,
        in_keys=["observation"],
        out_keys=["loc", "scale"],
    )
    actor = ProbabilisticActor(
        module=policy_module,
        in_keys=["loc", "scale"],
        spec=action_spec,
        distribution_class=TanhNormal,
    )
    qvalue = ValueOperator(
        module=nn.Linear(n_obs + n_act, 1),
        in_keys=["observation", "action"],
    )
    return SACLoss(actor_network=actor, qvalue_network=qvalue, action_spec=action_spec)


def main() -> int:
    loss = build_loss()
    observed = float(loss.target_entropy)
    expected = -2.0

    print(f"observed_target_entropy={observed}")
    print(f"expected_target_entropy={expected}")
    print(f"actor_spec_shape={loss.actor_network.spec.shape}")
    print(f"loss_action_spec_shape={loss._action_spec.shape}")

    if observed != expected:
        print(
            "Mismatch: SACLoss(target_entropy='auto') collapses a 2D action spec "
            "to -1 instead of -2."
        )
        return 1

    print("No mismatch observed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
