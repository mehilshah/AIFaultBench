#!/usr/bin/env python3
"""Repro probe for torch_geometric.data.data.BaseData importability."""

from __future__ import annotations

import sys


def main() -> int:
    try:
        import torch_geometric
        from torch_geometric.data.data import BaseData
    except Exception as exc:  # pragma: no cover - direct repro output
        print(f"IMPORT_FAIL {type(exc).__name__}: {exc}")
        return 1

    print(f"PYG_VERSION {torch_geometric.__version__}")
    print(f"IMPORT_OK {BaseData.__name__}")
    print(f"MODULE {BaseData.__module__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
