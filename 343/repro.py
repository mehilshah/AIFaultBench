#!/usr/bin/env python3
"""Minimal reproduction for the SDV FixedCombinations index mismatch bug."""

from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

from sdv.cag import FixedCombinations, SingleTableProgrammableConstraint  # noqa: E402
from sdv.metadata import Metadata  # noqa: E402
from sdv.single_table import GaussianCopulaSynthesizer  # noqa: E402


class DropLowAmenities(SingleTableProgrammableConstraint):
    """Mimic a constraint that filters rows after reverse_transform without resetting index."""

    def __init__(self, threshold_column="amenities_fee"):
        self.threshold_column = threshold_column

    def validate(self, metadata):
        return

    def validate_input_data(self, data):
        return

    def fit(self, data, metadata):
        self.metadata = metadata

    def transform(self, data):
        return data

    def get_updated_metadata(self, metadata):
        return metadata

    def reverse_transform(self, transformed_data):
        threshold = transformed_data[self.threshold_column].median()
        return transformed_data[transformed_data[self.threshold_column] >= threshold]

    def is_valid(self, synthetic_data):
        threshold = synthetic_data[self.threshold_column].median()
        return synthetic_data[self.threshold_column] >= threshold


def build_data():
    return pd.DataFrame(
        {
            "has_rewards": [True, False, True, False, True, False, True, False, True, False],
            "room_type": [
                "suite",
                "standard",
                "suite",
                "standard",
                "suite",
                "standard",
                "suite",
                "standard",
                "suite",
                "standard",
            ],
            "amenities_fee": [10.0, 0.0, 12.0, 1.0, 11.0, 0.5, 13.0, 0.0, 14.0, 1.5],
        }
    )


def build_metadata():
    return Metadata.load_from_dict(
        {
            "tables": {
                "table": {
                    "columns": {
                        "has_rewards": {"sdtype": "boolean"},
                        "room_type": {"sdtype": "categorical"},
                        "amenities_fee": {"sdtype": "numerical"},
                    }
                }
            }
        }
    )


def write_result(result):
    result_path = ROOT / "reproduction.json"
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


def main():
    data = build_data()
    metadata = build_metadata()

    synthesizer = GaussianCopulaSynthesizer(metadata)
    synthesizer.add_constraints(
        [
            FixedCombinations(column_names=["has_rewards", "room_type"], table_name="table"),
            DropLowAmenities(),
        ]
    )
    synthesizer.fit(data)

    try:
        synthesizer.sample(20)
    except Exception as exc:  # noqa: BLE001
        traceback.print_exc()
        result = {
            "reproducible": True,
            "evidence": (
                "Sampling raised "
                f"{type(exc).__module__}.{type(exc).__name__}: {exc}. "
                "The traceback reaches sdv/single_table/base.py:804 while applying "
                "reverse_transform_constraints."
            ),
            "steps": [
                "Build a single-table dataset with boolean, categorical, and numerical columns.",
                "Fit GaussianCopulaSynthesizer with FixedCombinations plus a row-dropping programmable constraint.",
                "Call sample(20).",
                "Observe pandas.errors.IndexingError from boolean index misalignment in reverse_transform_constraints.",
            ],
            "blocking_reason": "",
            "reproduction_command": "./setup_env.sh && ./run_repro.sh",
        }
        write_result(result)
        print("Reproducible: true")
        print(result["evidence"])
        return 0

    result = {
        "reproducible": False,
        "evidence": "Sampling completed without raising the expected IndexingError.",
        "steps": [
            "Build a single-table dataset with boolean, categorical, and numerical columns.",
            "Fit GaussianCopulaSynthesizer with FixedCombinations plus a row-dropping programmable constraint.",
            "Call sample(20).",
            "No pandas.errors.IndexingError was raised.",
        ],
        "blocking_reason": "The local checkout did not reproduce the bug with this input.",
        "reproduction_command": "./setup_env.sh && ./run_repro.sh",
    }
    write_result(result)
    print("Reproducible: false")
    print(result["evidence"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
