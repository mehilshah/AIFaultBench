#!/usr/bin/env python3
from __future__ import annotations

import traceback


def main() -> int:
    try:
        import eel  # noqa: F401
    except Exception as exc:  # pragma: no cover - used for repro output
        print(f"{type(exc).__name__}: {exc}")
        traceback.print_exc()
        return 1

    print("IMPORT_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
