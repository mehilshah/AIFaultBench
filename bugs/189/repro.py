#!/usr/bin/env python3
from __future__ import annotations

import sys
import traceback
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))


from open_clip.factory import load_state_dict  # noqa: E402


def main() -> int:
    checkpoint = ROOT / "codebase" / "logs" / "repro_train1" / "checkpoints" / "epoch_1.pt"
    print(f"checkpoint={checkpoint}")
    print("loading via open_clip.factory.load_state_dict(weights_only=True)")

    try:
        load_state_dict(str(checkpoint), device="cpu", weights_only=True)
    except Exception as exc:  # noqa: BLE001
        print(f"exception_type={type(exc).__name__}")
        traceback.print_exc()
        message = str(exc)
        if "Weights only load failed" in message or "Unsupported global: GLOBAL numpy.core.multiarray.scalar" in message:
            print("BUG_REPRODUCED")
            return 0
        print("UNEXPECTED_EXCEPTION")
        return 1

    print("UNEXPECTED_SUCCESS")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
