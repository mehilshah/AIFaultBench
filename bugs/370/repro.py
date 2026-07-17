#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import torch
from tensordict import TensorDict


ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR / "codebase"))

from torchrl.modules import LSTMModule  # noqa: E402
from torchrl.modules.tensordict_module.rnn import set_recurrent_mode  # noqa: E402


def main() -> None:
    torch.manual_seed(0)

    batch = 1
    time = 5
    features = 2
    hidden = 4

    is_init = torch.zeros(batch, time, 1, dtype=torch.bool)
    is_init[0, 3] = True

    obs = torch.ones(batch, time, features)
    obs[0, 3:] = 2.0

    data = TensorDict({"obs": obs, "is_init": is_init}, [batch, time])

    lstm = LSTMModule(
        input_size=features,
        hidden_size=hidden,
        in_key="obs",
        out_keys=[
            "action_features",
            ("next", "recurrent_state_h"),
            ("next", "recurrent_state_c"),
        ],
    )

    with set_recurrent_mode(True), torch.no_grad():
        data_recurrent = lstm(data)

    h = data_recurrent["next", "recurrent_state_h"]
    c = data_recurrent["next", "recurrent_state_c"]
    last_step_sum = h[0, -1].abs().sum().item()
    split_step_sum = h[0, 2].abs().sum().item()

    print("next.recurrent_state_h:")
    print(h)
    print("next.recurrent_state_c:")
    print(c)
    print(f"split_step_sum={split_step_sum:.6f}")
    print(f"last_step_sum={last_step_sum:.6f}")

    assert split_step_sum > 0, "The end of the first trajectory should carry state."
    assert (
        last_step_sum == 0
    ), "Expected the bug: the final step of the shorter trajectory is zeroed."
    print("BUG REPRODUCED")


if __name__ == "__main__":
    main()
