from __future__ import annotations

import argparse
import traceback

import torch
from tensordict import TensorDict
from torch import nn
from torch.nn import functional as F
from torchrl.data import Categorical
from torchrl.modules.tensordict_module.actors import ProbabilisticActor
from torchrl.modules.tensordict_module.common import SafeModule
from torchrl.objectives.iql import IQLLoss


def build_loss(action_shape: torch.Size) -> IQLLoss:
    n_act, n_obs = 4, 3
    action_spec = Categorical(n=n_act, shape=action_shape)
    net = nn.Sequential(nn.Linear(n_obs, n_act))
    module = SafeModule(net, in_keys=["observation"], out_keys=["logits"])
    actor = ProbabilisticActor(
        module=module,
        in_keys=["logits"],
        spec=action_spec,
        distribution_class=torch.distributions.Categorical,
    )

    class QValueClass(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.linear = nn.Linear(n_obs + n_act, 1)

        def forward(self, obs, act):
            return self.linear(torch.cat([obs, F.one_hot(act.squeeze(-1), n_act)], -1))

    qvalue = SafeModule(
        QValueClass(),
        in_keys=["observation", "action"],
        out_keys=["state_action_value"],
    )
    value = SafeModule(
        nn.Linear(n_obs, 1),
        in_keys=["observation"],
        out_keys=["state_value"],
    )
    return IQLLoss(actor, qvalue, value)


def make_batch(action_spec: Categorical) -> TensorDict:
    batch = [2]
    action = action_spec.rand(batch)
    return TensorDict(
        {
            "observation": torch.randn(*batch, 3),
            "action": action,
            ("next", "done"): torch.zeros(*batch, 1, dtype=torch.bool),
            ("next", "terminated"): torch.zeros(*batch, 1, dtype=torch.bool),
            ("next", "reward"): torch.randn(*batch, 1),
            ("next", "observation"): torch.randn(*batch, 3),
        },
        batch,
    )


def run_case(action_shape: torch.Size, label: str) -> None:
    loss = build_loss(action_shape)
    action_spec = Categorical(n=4, shape=action_shape)
    data = make_batch(action_spec)
    print(f"[{label}] action.shape = {tuple(data['action'].shape)}")
    try:
        out = loss(data)
    except Exception as exc:  # intentional: capture the failure as evidence
        print(f"[{label}] expected failure: {type(exc).__name__}: {exc}")
        traceback.print_exc()
        return
    print(f"[{label}] succeeded")
    print(f"[{label}] loss keys = {list(out.keys())}")
    print(f"[{label}] loss_actor = {out['loss_actor'].item():.10f}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("bug", "workaround", "both"),
        default="both",
        help="Run the failing shape, the working shape, or both.",
    )
    args = parser.parse_args()

    torch.manual_seed(0)
    print(f"torch={torch.__version__}")
    try:
        import tensordict

        print(f"tensordict={tensordict.__version__}")
    except Exception as exc:  # pragma: no cover - informational only
        print(f"tensordict import failed: {exc}")

    if args.mode in {"bug", "both"}:
        run_case(torch.Size((1,)), "bug")
    if args.mode in {"workaround", "both"}:
        run_case(torch.Size(()), "workaround")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
