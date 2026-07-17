#!/usr/bin/env python3
"""Minimal reproduction for the utcfromtimestamp deprecation warning."""

from __future__ import annotations

import warnings
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"


def main() -> int:
    sys.path.insert(0, str(CODEBASE))

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", DeprecationWarning)

        from influxdb_client.client.write.point import EPOCH  # noqa: WPS433

    deprecations = [
        warning for warning in caught
        if issubclass(warning.category, DeprecationWarning)
        and "utcfromtimestamp" in str(warning.message)
    ]

    print(f"imported influxdb_client.client.write.point")
    print(f"epoch={EPOCH.isoformat()}")
    print(f"deprecation_warnings={len(deprecations)}")
    for warning in deprecations:
        print(f"warning={warning.category.__name__}: {warning.message}")

    if not deprecations:
        raise AssertionError(
            "Expected a DeprecationWarning from datetime.utcfromtimestamp(), "
            "but none was captured."
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
