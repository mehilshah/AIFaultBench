from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

from sdv.metadata import SingleTableMetadata  # noqa: E402


def build_metadata() -> SingleTableMetadata:
    return SingleTableMetadata.load_from_dict(
        {
            "columns": {
                "A": {"sdtype": "id"},
                "B": {"sdtype": "datetime", "datetime_format": "%Y-%m-%d"},
                "C": {"sdtype": "numerical"},
                "D": {"sdtype": "categorical"},
            }
        }
    )


def describe(label: str, action) -> bool:
    try:
        action()
    except Exception as exc:  # pragma: no cover - repro output only
        print(f"{label}: raised {type(exc).__name__}: {exc}")
        return False

    print(f"{label}: completed without error")
    return True


def main() -> int:
    validate_metadata = build_metadata()
    validate_metadata.primary_key = "A"
    validate_metadata.sequence_key = "A"

    setter_metadata = build_metadata()
    setter_metadata.set_sequence_key("A")

    validate_ok = describe("metadata.validate()", validate_metadata.validate)
    setter_ok = describe("set_primary_key('A')", lambda: setter_metadata.set_primary_key("A"))

    if validate_ok or setter_ok:
        print("BUG REPRODUCED: primary_key and sequence_key can point to the same column.")
        return 0

    print("BUG NOT REPRODUCED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
