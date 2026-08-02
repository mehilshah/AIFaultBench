#!/usr/bin/env python3
"""Offline reproduction for langflow issue #12775 at the pinned checkout."""

from __future__ import annotations

import ast
import importlib.util
import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "codebase/src/lfx/src/lfx/custom/validate.py"


def install_import_stubs() -> None:
    """Provide only validate.py's import-time dependencies; no services are called."""
    langchain_core = types.ModuleType("langchain_core")
    langchain_api = types.ModuleType("langchain_core._api")
    deprecation = types.ModuleType("langchain_core._api.deprecation")

    class LangChainDeprecationWarning(Warning):
        pass

    deprecation.LangChainDeprecationWarning = LangChainDeprecationWarning

    pydantic = types.ModuleType("pydantic")

    class ValidationError(Exception):
        pass

    pydantic.ValidationError = ValidationError

    lfx = types.ModuleType("lfx")
    lfx.__path__ = []
    field_typing = types.ModuleType("lfx.field_typing")
    constants = types.ModuleType("lfx.field_typing.constants")
    constants.CUSTOM_COMPONENT_SUPPORTED_TYPES = {}
    constants.DEFAULT_IMPORT_STRING = ""
    log = types.ModuleType("lfx.log")
    logger_module = types.ModuleType("lfx.log.logger")

    class Logger:
        def debug(self, *args, **kwargs):
            pass

    logger_module.logger = Logger()

    sys.modules.update(
        {
            "langchain_core": langchain_core,
            "langchain_core._api": langchain_api,
            "langchain_core._api.deprecation": deprecation,
            "pydantic": pydantic,
            "lfx": lfx,
            "lfx.field_typing": field_typing,
            "lfx.field_typing.constants": constants,
            "lfx.log": log,
            "lfx.log.logger": logger_module,
        }
    )


def load_pinned_validate_module():
    if not SOURCE.is_file():
        raise RuntimeError(f"Pinned source is missing: {SOURCE}; run bash setup_codebase.sh first")
    install_import_stubs()
    spec = importlib.util.spec_from_file_location("pinned_lfx_validate", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load the pinned validate.py module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    validate = load_pinned_validate_module()

    fixture = types.ModuleType("offline_alias_fixture")

    class OriginalName:
        pass

    fixture.OriginalName = OriginalName
    sys.modules[fixture.__name__] = fixture

    code = """\
from offline_alias_fixture import OriginalName as AliasedName

class MyComponent:
    constructed = AliasedName()
"""

    try:
        validate.create_class(code, "MyComponent")
    except ValueError as exc:
        expected = "Name error (possibly undefined variable): name 'AliasedName' is not defined"
        if str(exc) != expected:
            raise AssertionError(f"Unexpected validation failure: {exc!r}") from exc
        scope = validate.prepare_global_scope(ast.parse("from offline_alias_fixture import OriginalName as AliasedName"))
        if "OriginalName" not in scope or "AliasedName" in scope:
            raise AssertionError(f"Unexpected import scope: {sorted(set(scope) & {'OriginalName', 'AliasedName'})}")
        print(f"BUG REPRODUCED: {exc}")
        raise SystemExit(1)
    raise AssertionError("Aliased from-import unexpectedly succeeded; the pinned bug is absent")


if __name__ == "__main__":
    main()
