from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

import numpy as np
from gymnasium import spaces
from pettingzoo.utils.env import ParallelEnv

ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
if str(CODEBASE) not in sys.path:
    sys.path.insert(0, str(CODEBASE))

from torchrl.envs.libs.pettingzoo import PettingZooWrapper


class MaskedDropEnv(ParallelEnv):
    metadata = {"name": "masked_drop_env_v0"}

    def __init__(self):
        self.possible_agents = ["agent_0", "agent_1"]
        self.agents = list(self.possible_agents)
        self._step_count = 0
        self._observation_space = spaces.Dict(
            {
                "observation": spaces.Box(
                    low=0.0, high=1.0, shape=(1,), dtype=np.float32
                ),
                "action_mask": spaces.MultiBinary(2),
            }
        )
        self._action_space = spaces.Discrete(2)

    def observation_space(self, agent):
        return self._observation_space

    def action_space(self, agent):
        return self._action_space

    def reset(self, seed=None, options=None):
        self.agents = list(self.possible_agents)
        self._step_count = 0
        observations = {
            agent: {
                "observation": np.array([0.0], dtype=np.float32),
                "action_mask": np.array([1, 1], dtype=np.int8),
            }
            for agent in self.agents
        }
        infos = {agent: {} for agent in self.agents}
        return observations, infos

    def step(self, actions):
        self._step_count += 1
        self.agents = ["agent_0"]
        observations = {
            "agent_0": {
                "observation": np.array([1.0], dtype=np.float32),
                "action_mask": np.array([1, 0], dtype=np.int8),
            }
        }
        rewards = {"agent_0": 0.0, "agent_1": 1.0}
        terminations = {"agent_0": False, "agent_1": True}
        truncations = {"agent_0": False, "agent_1": False}
        infos = {"agent_0": {}}
        return observations, rewards, terminations, truncations, infos

    def close(self):
        pass


def run() -> dict:
    env = PettingZooWrapper(env=MaskedDropEnv(), use_mask=True, done_on_any=False)
    reset_td = env.reset()
    action_td = env.input_spec["full_action_spec"].zero()

    result = {
        "reproducible": False,
        "evidence": "",
        "steps": [
            "Create a custom PettingZoo ParallelEnv with two agents and per-agent action masks.",
            "Wrap it with torchrl.envs.libs.pettingzoo.PettingZooWrapper using use_mask=True and done_on_any=False.",
            "Reset the wrapper, then step once after the environment drops agent_1 from the active observation dict.",
        ],
        "blocking_reason": "",
        "reproduction_command": "./run_repro.sh",
    }

    try:
        env.step(action_td)
    except KeyError as err:
        result["reproducible"] = True
        result["evidence"] = (
            "KeyError raised from PettingZooWrapper._update_action_mask when "
            f"accessing a missing agent key: {err!r}."
        )
        print("Observed expected failure:", repr(err))
        traceback.print_exc()
    except Exception as err:
        result["reproducible"] = False
        result["blocking_reason"] = (
            "The reproduction hit an unexpected exception instead of the reported KeyError: "
            f"{type(err).__name__}: {err}"
        )
        result["evidence"] = traceback.format_exc()
        print("Unexpected failure:", repr(err))
        traceback.print_exc()
    else:
        result["reproducible"] = False
        result["blocking_reason"] = (
            "The wrapper did not raise KeyError on the missing agent path."
        )
        result["evidence"] = "No exception was raised."
        print("No error observed.")

    out_path = ROOT / "reproduction.json"
    out_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_path.name}")
    return result


if __name__ == "__main__":
    run()
