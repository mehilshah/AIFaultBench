#!/usr/bin/env python3
"""Reproduce SDV issue 2453.

The local codebase accepts metadata where the same child foreign key is used in
two different relationships. The expected behavior is to reject this schema.
"""

from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"


def _load_module(name: str, relpath: str):
    spec = importlib.util.spec_from_file_location(name, CODEBASE / relpath)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _install_stub_modules() -> None:
    sdv_pkg = types.ModuleType("sdv")
    sdv_pkg.__path__ = [str(CODEBASE / "sdv")]
    sys.modules["sdv"] = sdv_pkg

    metadata_pkg = types.ModuleType("sdv.metadata")
    metadata_pkg.__path__ = [str(CODEBASE / "sdv" / "metadata")]
    sys.modules["sdv.metadata"] = metadata_pkg

    class _DummyLogger:
        def debug(self, *args: Any, **kwargs: Any) -> None:
            pass

        def info(self, *args: Any, **kwargs: Any) -> None:
            pass

        def warning(self, *args: Any, **kwargs: Any) -> None:
            pass

        def error(self, *args: Any, **kwargs: Any) -> None:
            pass

        def exception(self, *args: Any, **kwargs: Any) -> None:
            pass

    logging_pkg = types.ModuleType("sdv.logging")
    logging_pkg.get_sdv_logger = lambda name: _DummyLogger()
    sys.modules["sdv.logging"] = logging_pkg

    errors_mod = types.ModuleType("sdv.errors")

    class InvalidDataError(Exception):
        pass

    class SDVVersionWarning(Warning):
        pass

    class SynthesizerInputError(Exception):
        pass

    class VersionError(Exception):
        pass

    errors_mod.InvalidDataError = InvalidDataError
    errors_mod.SDVVersionWarning = SDVVersionWarning
    errors_mod.SynthesizerInputError = SynthesizerInputError
    errors_mod.VersionError = VersionError
    sys.modules["sdv.errors"] = errors_mod

    version_mod = types.ModuleType("sdv.version")
    version_mod.public = "0"
    version_mod.enterprise = None
    version_mod.__version__ = "0"
    sys.modules["sdv.version"] = version_mod
    sdv_pkg.version = version_mod
    sdv_pkg.errors = errors_mod

    # Minimal rdt stubs used at module import time.
    rdt_pkg = types.ModuleType("rdt")
    rdt_pkg.__path__ = []
    sys.modules["rdt"] = rdt_pkg

    transformers_pkg = types.ModuleType("rdt.transformers")
    transformers_pkg.__path__ = []
    sys.modules["rdt.transformers"] = transformers_pkg

    validators_mod = types.ModuleType("rdt.transformers._validators")

    class AddressValidator:
        @staticmethod
        def validate(*args: Any, **kwargs: Any) -> None:
            return None

    class GPSValidator:
        @staticmethod
        def validate(*args: Any, **kwargs: Any) -> None:
            return None

    validators_mod.AddressValidator = AddressValidator
    validators_mod.GPSValidator = GPSValidator
    sys.modules["rdt.transformers._validators"] = validators_mod

    pii_pkg = types.ModuleType("rdt.transformers.pii")
    pii_pkg.__path__ = []
    sys.modules["rdt.transformers.pii"] = pii_pkg

    anonymization_mod = types.ModuleType("rdt.transformers.pii.anonymization")
    anonymization_mod.SDTYPE_ANONYMIZERS = {}
    anonymization_mod.is_faker_function = lambda *args: False
    sys.modules["rdt.transformers.pii.anonymization"] = anonymization_mod

    utils_mod = types.ModuleType("rdt.transformers.utils")
    utils_mod._GENERATORS = {}
    sys.modules["rdt.transformers.utils"] = utils_mod

    # Minimal graphviz stub used while importing visualization helpers.
    graphviz_mod = types.ModuleType("graphviz")

    class ExecutableNotFound(Exception):
        pass

    class Digraph:
        def __init__(self, *args: Any, **kwargs: Any):
            pass

        def node(self, *args: Any, **kwargs: Any) -> None:
            pass

        def edge(self, *args: Any, **kwargs: Any) -> None:
            pass

        def render(self, *args: Any, **kwargs: Any) -> None:
            pass

    graphviz_mod.Digraph = Digraph
    graphviz_mod.ExecutableNotFound = ExecutableNotFound
    graphviz_mod.FORMATS = {"png", "jpg", "pdf"}
    graphviz_mod.version = lambda: "0"
    sys.modules["graphviz"] = graphviz_mod

    # Avoid the constraints import chain pulled in by metadata_upgrader.
    metadata_upgrader_mod = types.ModuleType("sdv.metadata.metadata_upgrader")
    metadata_upgrader_mod.convert_metadata = lambda metadata: metadata
    sys.modules["sdv.metadata.metadata_upgrader"] = metadata_upgrader_mod


def main() -> int:
    _install_stub_modules()

    # Load the real metadata implementation from the local codebase.
    _load_module("sdv.metadata.errors", "sdv/metadata/errors.py")
    _load_module("sdv.metadata.utils", "sdv/metadata/utils.py")
    _load_module("sdv.metadata.visualization", "sdv/metadata/visualization.py")
    _load_module("sdv._utils", "sdv/_utils.py")
    _load_module("sdv.metadata.single_table", "sdv/metadata/single_table.py")
    _load_module("sdv.metadata.multi_table", "sdv/metadata/multi_table.py")
    metadata_mod = _load_module("sdv.metadata.metadata", "sdv/metadata/metadata.py")

    Metadata = metadata_mod.Metadata
    metadata = Metadata.load_from_dict(
        {
            "tables": {
                "A": {"primary_key": "id", "columns": {"id": {"sdtype": "id"}}},
                "B": {"primary_key": "id", "columns": {"id": {"sdtype": "id"}}},
                "C": {"columns": {"parent_id": {"sdtype": "id"}}},
            },
            "relationships": [
                {
                    "parent_table_name": "A",
                    "parent_primary_key": "id",
                    "child_table_name": "C",
                    "child_foreign_key": "parent_id",
                },
                {
                    "parent_table_name": "B",
                    "parent_primary_key": "id",
                    "child_table_name": "C",
                    "child_foreign_key": "parent_id",
                },
            ],
        }
    )

    try:
        metadata.validate()
    except Exception as exc:  # pragma: no cover - this would indicate a fixed bug
        print("UNEXPECTED_EXCEPTION")
        print(type(exc).__name__)
        print(exc)
        return 1

    print("VALIDATE_OK")
    print("BUG_REPRODUCED: duplicated foreign key reuse was accepted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
