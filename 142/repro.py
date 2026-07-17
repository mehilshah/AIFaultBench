#!/usr/bin/env python3
"""Minimal reproduction for the SafetensorError pickling failure."""

from multiprocessing.reduction import ForkingPickler

from safetensors import SafetensorError


def main() -> int:
    err = SafetensorError("boom")
    print(f"exception_class={err.__class__}")
    print(f"exception_module={err.__class__.__module__}")
    try:
        ForkingPickler.dumps(err)
    except Exception as exc:
        print(f"repro_result={type(exc).__name__}: {exc}")
        return 0

    print("repro_result=unexpected success")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
