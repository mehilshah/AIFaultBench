#!/usr/bin/env python3
"""Reproduce malformed PHOENIX_CLIENT_HEADERS parsing on the pinned checkout."""

import importlib.metadata
import importlib.util


def _load_parser():
    """Load the installed package's target module without its optional dependencies."""
    distribution = importlib.metadata.distribution("arize-phoenix-otel")
    assert distribution.version == "0.16.0", distribution.version
    settings_path = distribution.locate_file("phoenix/otel/settings.py")
    spec = importlib.util.spec_from_file_location("bug741_settings", settings_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parse_env_headers


def main() -> None:
    parse_env_headers = _load_parser()
    try:
        headers = parse_env_headers("x=a,bad")
    except ValueError as exc:
        expected = "not enough values to unpack (expected 2, got 1)"
        if str(exc) != expected:
            raise AssertionError(f"unexpected ValueError: {exc!r}") from exc
        print(f"OBSERVED BUG: parse_env_headers('x=a,bad') raised ValueError: {exc}")
        raise

    assert headers == {"x": "a"}, headers
    print("No bug observed: malformed segment was skipped")


if __name__ == "__main__":
    main()
