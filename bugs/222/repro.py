#!/usr/bin/env python3
"""Reproduce the Triton client constructor failure from the local codebase."""

from __future__ import annotations

import importlib.util
import logging
import sys
import traceback
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"


def _install_namespace_packages() -> None:
    """Avoid importing towhee/__init__.py and its unrelated heavy dependencies."""

    for name, rel_path in [
        ("towhee", CODEBASE / "towhee"),
        ("towhee.serve", CODEBASE / "towhee" / "serve"),
        ("towhee.serve.triton", CODEBASE / "towhee" / "serve" / "triton"),
        ("towhee.utils", CODEBASE / "towhee" / "utils"),
    ]:
        module = types.ModuleType(name)
        module.__path__ = [str(rel_path)]
        sys.modules[name] = module


def _install_minimal_stubs() -> None:
    """Stub only the modules that are unrelated to the reported failure."""

    serializer = types.ModuleType("towhee.utils.serializer")
    serializer.to_json = lambda obj: str(obj)
    serializer.from_json = lambda data: data
    sys.modules["towhee.utils.serializer"] = serializer

    log_mod = types.ModuleType("towhee.utils.log")
    log_mod.engine_log = logging.getLogger("towhee.engine")
    sys.modules["towhee.utils.log"] = log_mod


def load_client_class():
    module_path = CODEBASE / "towhee" / "serve" / "triton" / "pipeline_client.py"
    spec = importlib.util.spec_from_file_location(
        "towhee.serve.triton.pipeline_client",
        module_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {module_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.Client


def main() -> int:
    _install_namespace_packages()
    _install_minimal_stubs()

    client_cls = load_client_class()
    print(f"Loaded {client_cls.__module__}.{client_cls.__name__} from {CODEBASE}")

    try:
        client_cls("127.0.0.1:8000")
    except Exception:  # pylint: disable=broad-except
        print("Reproduced bug: Client construction raises an exception.", file=sys.stderr)
        traceback.print_exc()
        return 0

    print("Bug not reproduced: Client constructed successfully.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
