#!/usr/bin/env python3
import json
from pathlib import Path
import sys


def main() -> int:
    target = Path("codebase/docs/deepvariant-details.md")
    expected = "# DeepVariant usage guide"

    if not target.exists():
        print(f"missing file: {target}", file=sys.stderr)
        return 2

    first_line = target.read_text(encoding="utf-8").splitlines()[0]
    reproduced = first_line != expected

    print(json.dumps({
        "file": str(target),
        "expected_first_line": expected,
        "observed_first_line": first_line,
        "reproduced": reproduced,
    }, indent=2))

    return 0 if reproduced else 1


if __name__ == "__main__":
    raise SystemExit(main())
