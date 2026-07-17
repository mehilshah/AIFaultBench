#!/usr/bin/env python3
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
sys.path.insert(0, str(CODEBASE))


def main() -> int:
    import timm

    models = timm.list_models("*faster*")
    print(f"timm_file={timm.__file__}")
    print(f"matches={[m for m in models if 'fasternet' in m]}")
    print(f"contains_fasternet_l={'fasternet_l' in models}")

    try:
        model = timm.create_model("fasternet_l.in1k", pretrained=False)
        print(f"create_model=OK {type(model).__name__}")
    except Exception as exc:  # pragma: no cover - for manual reproduction only
        print(f"{type(exc).__name__}: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
