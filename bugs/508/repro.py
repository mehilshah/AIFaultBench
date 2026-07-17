#!/usr/bin/env python3
"""Trigger the import-time failure described in the bug report."""

import traceback


def main() -> int:
    try:
        import numpyro  # noqa: F401
    except Exception as exc:  # pragma: no cover - used for repro output
        print(f"IMPORT_FAILED: {type(exc).__name__}: {exc}")
        traceback.print_exc()
        return 1

    print("IMPORT_SUCCEEDED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
