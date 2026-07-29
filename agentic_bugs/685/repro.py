#!/usr/bin/env python3
"""Reproduce langchain#38717 without making any provider calls."""


def main() -> None:
    try:
        from langchain.agents.middleware import PIIMatch  # noqa: F401
    except ImportError as exc:
        expected = "cannot import name 'PIIMatch' from 'langchain.agents.middleware'"
        if expected not in str(exc):
            raise AssertionError(f"unexpected ImportError: {exc}") from exc
        print(f"BUG REPRODUCED: public PIIMatch import raised ImportError: {exc}")
        raise SystemExit(1)
    raise AssertionError("bug not present: PIIMatch imported from the public package")


if __name__ == "__main__":
    main()
