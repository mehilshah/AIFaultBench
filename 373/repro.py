from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys
import types


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"


def ensure_package(name, path):
    module = sys.modules.get(name)
    if module is None:
        module = types.ModuleType(name)
        module.__path__ = [str(path)]
        module.__package__ = name
        sys.modules[name] = module
    return module


def load_module(name, relative_path):
    spec = spec_from_file_location(name, CODEBASE / relative_path)
    module = module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def bootstrap_sdv():
    sdv_pkg = ensure_package("sdv", CODEBASE / "sdv")

    version_module = types.ModuleType("sdv.version")
    version_module.community = "0.0.0"
    version_module.enterprise = None
    version_module.__all__ = ("community", "enterprise")
    sys.modules["sdv.version"] = version_module
    sdv_pkg.version = version_module

    ensure_package("sdv.logging", CODEBASE / "sdv" / "logging")
    ensure_package("sdv.constraints", CODEBASE / "sdv" / "constraints")
    ensure_package("sdv.metadata", CODEBASE / "sdv" / "metadata")

    load_module("sdv.errors", "sdv/errors.py")

    logging_utils = load_module("sdv.logging.utils", "sdv/logging/utils.py")
    logging_logger = load_module("sdv.logging.logger", "sdv/logging/logger.py")
    sdv_pkg.logging = sys.modules["sdv.logging"]
    sys.modules["sdv.logging"].get_sdv_logger = logging_logger.get_sdv_logger
    sys.modules["sdv.logging"].get_sdv_logger_config = logging_utils.get_sdv_logger_config

    load_module("sdv.metadata.errors", "sdv/metadata/errors.py")
    load_module("sdv.metadata.utils", "sdv/metadata/utils.py")
    load_module("sdv.metadata.visualization", "sdv/metadata/visualization.py")

    load_module("sdv._utils", "sdv/_utils.py")

    load_module("sdv.constraints.errors", "sdv/constraints/errors.py")
    load_module("sdv.constraints.utils", "sdv/constraints/utils.py")
    constraints_base = load_module("sdv.constraints.base", "sdv/constraints/base.py")
    constraints_tabular = load_module("sdv.constraints.tabular", "sdv/constraints/tabular.py")

    constraints_pkg = sys.modules["sdv.constraints"]
    constraints_pkg.Constraint = constraints_base.Constraint
    constraints_pkg.FixedCombinations = constraints_tabular.FixedCombinations
    constraints_pkg.FixedIncrements = constraints_tabular.FixedIncrements
    constraints_pkg.Inequality = constraints_tabular.Inequality
    constraints_pkg.Negative = constraints_tabular.Negative
    constraints_pkg.OneHotEncoding = constraints_tabular.OneHotEncoding
    constraints_pkg.Positive = constraints_tabular.Positive
    constraints_pkg.Range = constraints_tabular.Range
    constraints_pkg.ScalarInequality = constraints_tabular.ScalarInequality
    constraints_pkg.ScalarRange = constraints_tabular.ScalarRange
    constraints_pkg.Unique = constraints_tabular.Unique
    constraints_pkg.create_custom_constraint_class = (
        constraints_tabular.create_custom_constraint_class
    )

    load_module("sdv.metadata.metadata_upgrader", "sdv/metadata/metadata_upgrader.py")
    load_module("sdv.metadata.single_table", "sdv/metadata/single_table.py")
    load_module("sdv.metadata.multi_table", "sdv/metadata/multi_table.py")
    metadata_module = load_module("sdv.metadata.metadata", "sdv/metadata/metadata.py")
    return metadata_module.Metadata


def main():
    Metadata = bootstrap_sdv()
    metadata = Metadata.load_from_dict(
        {
            "tables": {
                "parent": {
                    "columns": {
                        "pk": {"sdtype": "id"},
                        "other": {"sdtype": "categorical"},
                    },
                    "primary_key": "pk",
                },
                "child": {
                    "columns": {
                        "fk": {"sdtype": "id"},
                    },
                },
            },
            "relationships": [
                {
                    "parent_table_name": "parent",
                    "child_table_name": "child",
                    "parent_primary_key": "other",
                    "child_foreign_key": "fk",
                }
            ],
        }
    )

    graph = metadata.visualize()
    source = graph.source
    print(source)
    print("contains_fk_to_other:", "fk → other" in source)
    print("contains_fk_to_pk:", "fk → pk" in source)

    assert "fk → other" in source, f"Expected relationship label 'fk → other' but got:\n{source}"


if __name__ == "__main__":
    main()
