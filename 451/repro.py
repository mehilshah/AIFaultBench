from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))

from lightning.pytorch import Trainer
from lightning.pytorch.cli import LightningArgumentParser


def main() -> int:
    parser = LightningArgumentParser()
    parser.add_lightning_class_args(Trainer, "trainer")

    config = {
        "trainer": {
            "strategy": {
                "class_path": "lightning.pytorch.strategies.FSDPStrategy",
                "init_args": {
                    "sharding_strategy": "HYBRID_SHARD",
                    "device_mesh": [1, 4],
                },
            },
        }
    }

    try:
        parser.parse_object(config)
    except SystemExit as exc:
        if exc.code not in (None, 0):
            print("EXPECTED_FAILURE: parser rejected trainer.strategy.device_mesh=[1, 4]")
            return 0
        return 0

    print("UNEXPECTED_SUCCESS: parser accepted trainer.strategy.device_mesh=[1, 4]")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
