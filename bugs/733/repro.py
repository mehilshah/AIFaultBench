#!/usr/bin/env python3
"""Reproduce mem0-cli's uncaught integer-config conversion error."""

from mem0_cli.config import Mem0Config, set_nested_value


config = Mem0Config()
original_version = config.version

try:
    set_nested_value(config, "version", "abc")
except ValueError as error:
    expected = "invalid literal for int() with base 10: 'abc'"
    assert str(error) == expected, repr(error)
    assert config.version == original_version, config.version
    print(f"BUG REPRODUCED: set_nested_value raised ValueError: {error}")
    raise
else:
    raise AssertionError(
        "BUG NOT PRESENT: a non-numeric integer config value did not raise ValueError"
    )
