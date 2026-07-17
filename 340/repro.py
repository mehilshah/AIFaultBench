from __future__ import annotations

import copy

import torch.nn as nn
from tensordict import TensorDict
from tensordict.nn import TensorDictModule
from torchrl.collectors import Evaluator
from torchrl.envs import GymEnv


def _state_dict_keys(module: nn.Module) -> int:
    return len(module.state_dict())


def main() -> None:
    policy_bug = TensorDictModule(nn.Linear(4, 2), ["observation"], ["action"])

    print("=== BUG ===")
    print(f"state_dict before: {_state_dict_keys(policy_bug)} keys")

    evaluator = Evaluator(lambda: GymEnv("CartPole-v1"), policy_bug, max_steps=10)
    try:
        evaluator.evaluate(TensorDict.from_module(policy_bug).data)
    finally:
        evaluator.shutdown()

    after = _state_dict_keys(policy_bug)
    print(f"state_dict after:  {after} keys")
    print(policy_bug.state_dict())
    assert after == 0, "Expected evaluate(weights=nn.Module) to empty state_dict()"

    policy_fix = TensorDictModule(nn.Linear(4, 2), ["observation"], ["action"])

    print("=== WORKAROUND ===")
    print(f"state_dict before: {_state_dict_keys(policy_fix)} keys")

    eval_copy = copy.deepcopy(policy_fix)
    evaluator_fix = Evaluator(lambda: GymEnv("CartPole-v1"), eval_copy, max_steps=10)
    weights = TensorDict.from_module(policy_fix).data.detach().clone().cpu()
    try:
        evaluator_fix.evaluate(weights)
    finally:
        evaluator_fix.shutdown()

    after_fix = _state_dict_keys(policy_fix)
    print(f"state_dict after:  {after_fix} keys")
    print(policy_fix.state_dict())
    assert after_fix == 2, "Expected the workaround to preserve state_dict()"
    print("PASS")


if __name__ == "__main__":
    main()
