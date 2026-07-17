from __future__ import annotations

import sys
import traceback


def main() -> int:
    try:
        sys.path.insert(0, "codebase")
        from flair.datasets import WIKINER_FRENCH  # noqa: F401
    except Exception as exc:  # pragma: no cover - repro script
        traceback.print_exc()
        if isinstance(exc, ImportError) and "WIKINER_FRENCH" in str(exc):
            print("EXPECTED_FAILURE: missing flair.datasets.WIKINER_FRENCH")
            return 0

        print(f"UNEXPECTED_FAILURE: {type(exc).__name__}: {exc}")
        return 1

    print("UNEXPECTED_SUCCESS: flair.datasets.WIKINER_FRENCH imported")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
