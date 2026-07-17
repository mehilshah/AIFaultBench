#!/usr/bin/env python3
"""Minimal reproduction harness for SDV issue 2825.

This loader avoids SDV's top-level import side effects and loads just the
metadata modules needed for the reported `set_primary_key()` path.
"""

from __future__ import annotations

import importlib.util
import sys
import traceback
import types
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
CODEBASE_SDV = ROOT / "codebase" / "sdv"


def _stub_module(name: str, **attrs):
    module = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    sys.modules[name] = module
    return module


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {name} from {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _bootstrap_sdv_imports():
    # Create a lightweight package skeleton so we can import source files
    # directly without executing sdv.__init__ and its optional dependency tree.
    sdv_pkg = _stub_module("sdv")
    sdv_pkg.__path__ = [str(CODEBASE_SDV)]

    metadata_pkg = _stub_module("sdv.metadata")
    metadata_pkg.__path__ = [str(CODEBASE_SDV / "metadata")]

    version_mod = _stub_module(
        "sdv.version",
        community="1.34.2.dev0",
        __version__="1.34.2.dev0",
    )
    sdv_pkg.version = version_mod

    logging_mod = _stub_module("sdv.logging")

    def get_sdv_logger(name):
        import logging

        return logging.getLogger(name)

    logging_mod.get_sdv_logger = get_sdv_logger
    sdv_pkg.logging = logging_mod

    # The metadata visualization helpers are only imported at module import
    # time for type/utility references; the repro never calls them.
    _stub_module(
        "sdv.metadata.visualization",
        create_columns_node=lambda columns: "",
        create_summarized_columns_node=lambda columns: "",
        visualize_graph=lambda *args, **kwargs: None,
    )

    # The current repro does not rely on metadata conversion.
    _stub_module("sdv.metadata.metadata_upgrader", convert_metadata=lambda metadata: metadata)

    # Minimal RDT shims. The metadata modules only need the importable symbols.
    _stub_module("rdt")
    _stub_module("rdt.transformers")

    class _Validator:
        @staticmethod
        def validate(*args, **kwargs):
            return True

    _stub_module(
        "rdt.transformers._validators",
        AddressValidator=_Validator,
        GPSValidator=_Validator,
    )
    _stub_module("rdt.transformers.pii")
    _stub_module(
        "rdt.transformers.pii.anonymization",
        SDTYPE_ANONYMIZERS={},
        is_faker_function=lambda value: False,
    )
    _stub_module(
        "rdt.transformers.utils",
        _GENERATORS={},
        strings_from_regex=lambda regex, size: ["x"] * size,
    )

    _load_module("sdv.errors", CODEBASE_SDV / "errors.py")
    _load_module("sdv.metadata.errors", CODEBASE_SDV / "metadata" / "errors.py")
    _load_module("sdv.metadata.utils", CODEBASE_SDV / "metadata" / "utils.py")
    _load_module("sdv._utils", CODEBASE_SDV / "_utils.py")
    _load_module("sdv.metadata.single_table", CODEBASE_SDV / "metadata" / "single_table.py")
    _load_module("sdv.metadata.multi_table", CODEBASE_SDV / "metadata" / "multi_table.py")
    metadata_module = _load_module("sdv.metadata.metadata", CODEBASE_SDV / "metadata" / "metadata.py")
    metadata_pkg.Metadata = metadata_module.Metadata


def main():
    _bootstrap_sdv_imports()

    from sdv.metadata import Metadata

    print("Loaded Metadata from local source tree.")
    print("Running the reported duplicate-primary-key setup...")

    metadata = Metadata.load_from_dict(
        {
            "tables": {
                "accounts": {
                    "columns": {
                        "user_id": {"sdtype": "id", "regex_format": "ID_[0-9]{1,2}"},
                        "account_type": {"sdtype": "categorical"},
                        "col1": {"sdtype": "categorical"},
                        "col2": {"sdtype": "categorical"},
                    }
                }
            }
        }
    )

    metadata.set_primary_key(["user_id", "user_id"], table_name="accounts")
    print("Stored primary key:", metadata.tables["accounts"].primary_key)

    data = pd.DataFrame(
        {
            "user_id": ["ID_1", "ID_2"],
            "account_type": ["a", "b"],
            "col1": ["x", "y"],
            "col2": ["m", "n"],
        }
    )

    print("Calling validate_data(...)")
    metadata.validate_data({"accounts": data})
    print("No exception raised.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        raise SystemExit(1)
