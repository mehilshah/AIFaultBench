from __future__ import annotations

import json
import sys
import types
from dataclasses import dataclass, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CODEBASE_SRC = ROOT / "codebase" / "src"


def _install_package(name: str, path: Path) -> None:
    package = types.ModuleType(name)
    package.__path__ = [str(path)]
    sys.modules[name] = package


if str(CODEBASE_SRC) not in sys.path:
    sys.path.insert(0, str(CODEBASE_SRC))

_install_package("lightning", CODEBASE_SRC / "lightning")
_install_package("lightning.fabric", CODEBASE_SRC / "lightning" / "fabric")
_install_package("lightning.fabric.utilities", CODEBASE_SRC / "lightning" / "fabric" / "utilities")

from lightning.fabric.utilities.distributed import DistributedSamplerWrapper
from torch.utils.data import Sampler


@dataclass
class Result:
    reproducible: bool
    evidence: str
    steps: list[str]
    blocking_reason: str
    reproduction_command: str


class RecordingSampler(Sampler[int]):
    def __init__(self, items: list[int]) -> None:
        self.items = list(items)
        self.set_epoch_calls: list[int] = []

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def set_epoch(self, epoch: int) -> None:
        self.set_epoch_calls.append(epoch)


def main() -> int:
    sampler = RecordingSampler([0, 1, 2, 3])
    wrapper = DistributedSamplerWrapper(sampler, num_replicas=1, rank=0, shuffle=False)

    wrapper.set_epoch(7)

    reproducible = sampler.set_epoch_calls == []
    evidence = (
        "DistributedSamplerWrapper.set_epoch(7) did not forward to the wrapped sampler: "
        f"sampler.set_epoch_calls={sampler.set_epoch_calls}, wrapper.epoch={wrapper.epoch}"
    )
    result = Result(
        reproducible=reproducible,
        evidence=evidence,
        steps=[
            "Create a custom sampler that records set_epoch calls.",
            "Wrap it with DistributedSamplerWrapper(num_replicas=1, rank=0, shuffle=False).",
            "Call wrapper.set_epoch(7) and inspect the wrapped sampler.",
        ],
        blocking_reason="" if reproducible else "The wrapper forwarded set_epoch to the wrapped sampler.",
        reproduction_command="bash run_repro.sh",
    )

    out_path = ROOT / "reproduction.json"
    out_path.write_text(json.dumps(asdict(result), indent=2) + "\n", encoding="utf-8")
    print(evidence)
    print(f"Wrote result to {out_path}")
    return 0 if reproducible else 1


if __name__ == "__main__":
    raise SystemExit(main())
