from __future__ import annotations

import sys
from pathlib import Path

import torch
from torch import nn

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

from torchrl.modules.models.multiagent import MultiAgentNetBase  # noqa: E402


class SingleAgentMLP(nn.Module):
    def __init__(self, in_dim: int, out_dim: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, 64),
            nn.Tanh(),
            nn.Linear(64, out_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class MultiAgentPolicyNet(MultiAgentNetBase):
    def __init__(self, obs_dim: int, action_dim: int, n_agents: int, *, agent_dim: int):
        self.obs_dim = obs_dim
        self.action_dim = action_dim
        super().__init__(
            n_agents=n_agents,
            centralized=False,
            share_params=True,
            agent_dim=agent_dim,
            device=None,
        )

    def _build_single_net(self, *, device, **kwargs):
        net = SingleAgentMLP(self.obs_dim, 2 * self.action_dim)
        return net.to(device) if device is not None else net

    def _pre_forward_check(self, inputs):
        return inputs


def run_case(agent_dim: int) -> tuple[bool, str]:
    net = MultiAgentPolicyNet(obs_dim=5, action_dim=2, n_agents=3, agent_dim=agent_dim)
    x = torch.randn(4, 3, 6, 5)
    try:
        y = net(x)
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"
    return True, f"output_shape={tuple(y.shape)}"


def main() -> int:
    print("Torch:", torch.__version__)
    print("Input shape: (4, 3, 6, 5)")
    print("Configuration: share_params=True, centralized=False, n_agents=3")
    print()

    results = {}
    for agent_dim in (1, 0):
        ok, message = run_case(agent_dim)
        results[agent_dim] = ok
        status = "ok" if ok else "failed"
        print(f"agent_dim={agent_dim}: {status}")
        print(f"  {message}")

    reproduced = all(not ok for ok in results.values())
    print()
    print(f"reproduced={reproduced}")
    return 0 if reproduced else 1


if __name__ == "__main__":
    raise SystemExit(main())
