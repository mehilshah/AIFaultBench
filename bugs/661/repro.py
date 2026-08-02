#!/usr/bin/env python3
"""Trigger CrewAI's A2A SDK 1.0 import incompatibility without a network call."""

from pathlib import Path
from importlib.metadata import version
import sys
from types import ModuleType


source_root = Path(__file__).parent / "codebase" / "lib" / "crewai" / "src" / "crewai"

# Avoid CrewAI's top-level convenience imports: they load unrelated optional
# components before the A2A configuration path reached by the issue.
for module_name, package_path in (("crewai", source_root), ("crewai.a2a", source_root / "a2a")):
    package = ModuleType(module_name)
    package.__path__ = [str(package_path)]
    sys.modules[module_name] = package

from crewai.a2a.config import A2AClientConfig


try:
    A2AClientConfig(endpoint="http://localhost:8888/.well-known/agent-card.json")
except ImportError as exc:
    expected = "cannot import name 'A2AClientHTTPError' from 'a2a.client.errors'"
    assert expected in str(exc), f"unexpected ImportError: {exc!r}"
    assert version("a2a-sdk") == "1.0.1"
    print(f"OBSERVED BUG with a2a-sdk 1.0.1: {exc}")
    raise
else:
    raise AssertionError(
        "BUG NOT OBSERVED: A2AClientConfig unexpectedly initialized with a2a-sdk 1.0.1"
    )
