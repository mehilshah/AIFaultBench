#!/usr/bin/env python3
"""Minimal reproduction for Equinox Module method lookup invoking __getattr__.

The bug report describes `eqx.Module` methods causing user-defined `__getattr__`
to run for `__name__` and `__qualname__` during normal method invocation.
"""

from __future__ import annotations

import json
from pathlib import Path

import equinox as eqx


ROOT = Path(__file__).resolve().parent


hits: list[str] = []


class Foo(eqx.Module):
    baz: str = "foobaz"

    def __getattr__(self, name):
        hits.append(name)
        print(f"__getattr__ hit: {name}")
        return "getattr"

    def moo(self):
        return "moo"


def main() -> int:
    foo = Foo()
    result = foo.moo()
    reproduced = set(hits) == {"__name__", "__qualname__"} and result == "moo"

    payload = {
        "instance_type": type(foo).__name__,
        "method_result": result,
        "getattr_hits": hits,
        "reproduced": reproduced,
        "repo_root": str(ROOT),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))

    if reproduced:
        print(
            "BUG REPRODUCED: invoking Foo().moo() calls user-defined __getattr__ twice."
        )
        return 1

    print("No reproduction: method invocation did not trigger the reported getattr hits.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
