#!/usr/bin/env python3
"""Reproduce SDV issue 2799 from the vendored source tree.

This script loads only the metadata modules needed for the bug so we do not
pull in unrelated synthesizer dependencies.
"""

from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent / "codebase" / "sdv"


def ensure_package(name: str, path: Path) -> types.ModuleType:
    module = types.ModuleType(name)
    module.__path__ = [str(path)]
    sys.modules[name] = module
    return module


def load_module(name: str, path: Path) -> types.ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module {name} from {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_metadata_class():
    """Load ``Metadata`` without importing the full ``sdv`` package."""
    sdv_pkg = ensure_package("sdv", ROOT)
    ensure_package("sdv.metadata", ROOT / "metadata")
    ensure_package("sdv.logging", ROOT / "logging")

    version_mod = types.ModuleType("sdv.version")
    version_mod.community = "1.33.1.dev0"
    version_mod.enterprise = None
    sys.modules["sdv.version"] = version_mod
    setattr(sdv_pkg, "version", version_mod)

    load_module("sdv.errors", ROOT / "errors.py")
    load_module("sdv.logging.utils", ROOT / "logging" / "utils.py")
    load_module("sdv.logging.logger", ROOT / "logging" / "logger.py")
    load_module("sdv.logging", ROOT / "logging" / "__init__.py")
    load_module("sdv._utils", ROOT / "_utils.py")
    load_module("sdv.metadata.errors", ROOT / "metadata" / "errors.py")
    load_module("sdv.metadata.utils", ROOT / "metadata" / "utils.py")
    load_module("sdv.metadata.visualization", ROOT / "metadata" / "visualization.py")

    metadata_upgrader = types.ModuleType("sdv.metadata.metadata_upgrader")

    def convert_metadata(metadata):
        return metadata

    metadata_upgrader.convert_metadata = convert_metadata
    sys.modules["sdv.metadata.metadata_upgrader"] = metadata_upgrader

    load_module("sdv.metadata.single_table", ROOT / "metadata" / "single_table.py")
    load_module("sdv.metadata.multi_table", ROOT / "metadata" / "multi_table.py")
    metadata_mod = load_module("sdv.metadata.metadata", ROOT / "metadata" / "metadata.py")
    return metadata_mod.Metadata


def main() -> int:
    Metadata = load_metadata_class()

    data = {
        "parent": pd.DataFrame(
            {
                "email": ["sdv@sdv.dev", "info@datacebo.com", "info@gmail.com"],
            }
        ),
        "child": pd.DataFrame(
            {
                "child_id": [1, 2],
                "email": ["sdv@sdv.dev", "sdv@sdv.dev"],
            }
        ),
    }

    metadata = Metadata().detect_from_dataframes(
        data, foreign_key_inference_algorithm="column_name_match"
    )

    expected_relationship = {
        "parent_table_name": "parent",
        "parent_primary_key": "email",
        "child_table_name": "child",
        "child_foreign_key": "email",
    }

    print("Expected one relationship for semantic foreign key detection.")
    print(f"Expected relationship: {expected_relationship}")
    print(f"Actual relationships: {metadata.relationships}")
    print(metadata.to_dict())

    assert metadata.relationships == [
        expected_relationship
    ], "semantic foreign key was not detected"
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
