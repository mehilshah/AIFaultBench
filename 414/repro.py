#!/usr/bin/env python3
from __future__ import annotations

import json
import platform
import sys


def _emit(message: str) -> None:
    print(message, flush=True)


def main() -> int:
    _emit(
        json.dumps(
            {
                "platform": platform.platform(),
                "system": platform.system(),
                "python": sys.version.split()[0],
            },
            indent=2,
        )
    )

    if platform.system() != "Darwin":
        _emit(
            "BLOCKED: the reported bug is MPS-specific and requires macOS; "
            f"this host is {platform.system()}."
        )
        return 2

    try:
        import torch
    except Exception as exc:  # pragma: no cover - environment dependent
        _emit(f"BLOCKED: failed to import torch: {exc!r}")
        return 2

    mps_backend = getattr(torch.backends, "mps", None)
    if mps_backend is None or not mps_backend.is_available():
        _emit("BLOCKED: torch.backends.mps.is_available() is false on this host.")
        return 2

    from tensordict import TensorDict, TensorDictBase
    from torchrl.data.tensor_specs import Unbounded
    from torchrl.envs import EnvBase, SerialEnv

    class Float64ObsEnv(EnvBase):
        def __init__(self, **kwargs):
            self.observation_spec = Unbounded(shape=(3,), dtype=torch.float64)
            self.action_spec = Unbounded(shape=(1,), dtype=torch.int64)
            super().__init__(**kwargs)

        def _reset(self, tensordict: TensorDictBase, **kwargs) -> TensorDictBase:
            return TensorDict(
                {
                    "observation": torch.zeros(3, dtype=torch.float64),
                    "done": torch.zeros(1, dtype=torch.bool),
                    "terminated": torch.zeros(1, dtype=torch.bool),
                },
                batch_size=self.batch_size,
                device=self.device,
            )

        def _step(self, tensordict: TensorDictBase, **kwargs) -> TensorDictBase:
            return TensorDict(
                {
                    "observation": torch.ones(3, dtype=torch.float64),
                    "reward": torch.zeros(1, dtype=torch.float64),
                    "done": torch.zeros(1, dtype=torch.bool),
                    "terminated": torch.zeros(1, dtype=torch.bool),
                },
                batch_size=self.batch_size,
                device=self.device,
            )

        def _set_seed(self, seed: int | None) -> None:
            return None

    _emit("MPS is available. Running the TorchRL repro.")
    with torch.no_grad():
        spec = Unbounded(shape=(6,), device="cpu", dtype=torch.float64)
        downcast_spec = spec.to("mps")
        _emit(
            f"Unbounded.to('mps') -> dtype={downcast_spec.dtype}, "
            f"device={downcast_spec.device}"
        )

        env = SerialEnv(2, lambda: Float64ObsEnv(), device="mps")
        reset_td = env.reset()
        _emit(f"SerialEnv.reset() completed with device={reset_td.device}")
        _emit(f"Reset keys: {sorted(reset_td.keys(True, True))}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
