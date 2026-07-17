#!/usr/bin/env python3
from __future__ import annotations

import os
import sys

import torch
from tensordict import TensorDict

sys.path.insert(0, os.path.abspath("codebase"))

from torchrl.data import Binary, Categorical, Composite, Unbounded  # noqa: E402
from torchrl.envs import EnvBase  # noqa: E402
from torchrl.envs.utils import check_env_specs  # noqa: E402


class MiniMultiAgentEnv(EnvBase):
    def __init__(self):
        super().__init__(device="cpu", batch_size=torch.Size([2]))

        self.observation_spec = Composite(
            {
                "timestep": Unbounded(shape=torch.Size([2]), dtype=torch.int64),
                "agents": Composite(
                    {
                        "observations": Categorical(
                            n=40,
                            shape=torch.Size([2, 3, 4]),
                            dtype=torch.int64,
                        ),
                        "action_mask": Binary(
                            n=5,
                            shape=torch.Size([2, 3, 5]),
                            dtype=torch.bool,
                        ),
                    },
                    shape=torch.Size([2, 3]),
                ),
            },
            shape=torch.Size([2]),
        )

        self.state_spec = Composite(
            {
                "randomStates": Unbounded(
                    shape=torch.Size([2, 6]),
                    dtype=torch.uint8,
                ),
                "agents": Composite(
                    {
                        "rewards": Unbounded(
                            shape=torch.Size([2, 3, 1]),
                            dtype=torch.float32,
                        ),
                    },
                    shape=torch.Size([2, 3]),
                ),
            },
            shape=torch.Size([2]),
        )

        self.action_spec = Composite(
            {
                "agents": Composite(
                    {
                        "actions": Categorical(
                            n=5,
                            shape=torch.Size([2, 3, 1]),
                            dtype=torch.int64,
                        ),
                    },
                    shape=torch.Size([2, 3]),
                ),
            },
            shape=torch.Size([2]),
        )

        self.reward_spec = Composite(
            {
                "agents": Composite(
                    {
                        "rewards": Unbounded(
                            shape=torch.Size([2, 3, 1]),
                            dtype=torch.float32,
                        ),
                    },
                    shape=torch.Size([2, 3]),
                ),
            },
            shape=torch.Size([2]),
        )

        self.done_spec = Composite(
            {
                "done": Categorical(
                    n=2,
                    shape=torch.Size([2, 1]),
                    dtype=torch.bool,
                ),
                "agents": Composite(
                    {
                        "stepDones": Categorical(
                            n=2,
                            shape=torch.Size([2, 3, 1]),
                            dtype=torch.bool,
                        ),
                    },
                    shape=torch.Size([2, 3]),
                ),
            },
            shape=torch.Size([2]),
        )

    def _set_seed(self, seed):
        self.seed = seed

    def _reset(self, tensordict=None, **kwargs):
        return TensorDict(
            {
                "timestep": torch.zeros(2, dtype=torch.int64),
                "randomStates": torch.zeros(2, 6, dtype=torch.uint8),
                "agents": TensorDict(
                    {
                        "observations": torch.zeros(2, 3, 4, dtype=torch.int64),
                        "action_mask": torch.zeros(2, 3, 5, dtype=torch.bool),
                        "rewards": torch.zeros(2, 3, 1),
                        "stepDones": torch.zeros(2, 3, 1, dtype=torch.bool),
                    },
                    batch_size=[2, 3],
                ),
            },
            batch_size=[2],
        )

    def _step(self, tensordict):
        return TensorDict(
            {
                "timestep": torch.ones(2, dtype=torch.int64),
                "randomStates": torch.ones(2, 6, dtype=torch.uint8),
                "agents": TensorDict(
                    {
                        "observations": torch.ones(2, 3, 4, dtype=torch.int64),
                        "action_mask": torch.ones(2, 3, 5, dtype=torch.bool),
                        "actions": torch.ones(2, 3, 1, dtype=torch.int64),
                        "rewards": torch.ones(2, 3, 1),
                        "stepDones": torch.zeros(2, 3, 1, dtype=torch.bool),
                    },
                    batch_size=[2, 3],
                ),
                "reward": torch.ones(2, 1),
                "done": torch.zeros(2, 1, dtype=torch.bool),
                "terminated": torch.zeros(2, 1, dtype=torch.bool),
            },
            batch_size=[2],
        )


def main():
    env = MiniMultiAgentEnv()

    fake = env.fake_tensordict()
    rollout = env.rollout(3, break_when_any_done=False)

    print("FAKE_KEYS", sorted(map(str, fake.keys(True, True))))
    print("ROLLOUT_KEYS", sorted(map(str, rollout.keys(True, True))))

    check_env_specs(env, break_when_any_done=False)


if __name__ == "__main__":
    main()
