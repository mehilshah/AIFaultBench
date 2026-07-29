#!/usr/bin/env python3
"""Offline reproduction for Langflow custom-component future annotations bug."""

import ast
import importlib.util
import sys
import types
from pathlib import Path


def install_module(name: str, **attributes: object) -> types.ModuleType:
    module = types.ModuleType(name)
    module.__dict__.update(attributes)
    sys.modules[name] = module
    return module


class _Logger:
    def debug(self, *args: object, **kwargs: object) -> None:
        pass


def load_pinned_validate_module() -> types.ModuleType:
    """Load the checkout's unmodified validate.py without installing Langflow."""
    install_module("langchain_core")
    install_module("langchain_core._api")
    install_module(
        "langchain_core._api.deprecation", LangChainDeprecationWarning=DeprecationWarning
    )
    install_module("pydantic", ValidationError=ValueError)
    install_module("lfx")
    install_module("lfx.field_typing")
    install_module(
        "lfx.field_typing.constants",
        CUSTOM_COMPONENT_SUPPORTED_TYPES={},
        DEFAULT_IMPORT_STRING="",
    )
    install_module("lfx.log")
    install_module("lfx.log.logger", logger=_Logger())

    source = Path(__file__).parent / "codebase/src/lfx/src/lfx/custom/validate.py"
    if not source.is_file():
        raise RuntimeError(f"Pinned source file is missing: {source}")
    spec = importlib.util.spec_from_file_location("pinned_lfx_validate", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load the pinned validate.py module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CUSTOM_COMPONENT = """
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from deliberately_unavailable_package import SomeType

class SandboxProbe:
    def build(self, value: SomeType) -> SomeType:
        return value
"""


validate = load_pinned_validate_module()
try:
    validate.prepare_global_scope(ast.parse(CUSTOM_COMPONENT))
except NameError as error:
    assert str(error) == "name 'SomeType' is not defined", repr(error)
    print("BUG REPRODUCED: NameError: name 'SomeType' is not defined")
    raise SystemExit(1)

raise AssertionError("BUG NOT PRESENT: future annotations were preserved by the sandbox")
