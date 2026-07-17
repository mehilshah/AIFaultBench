"""Reproduce the SDV Inequality datetime diagnostic regression."""

from __future__ import annotations

import sys
import warnings

import pandas as pd


def main() -> None:
    warnings.filterwarnings("ignore", category=FutureWarning)

    import sdv
    from sdv.cag import Inequality
    from sdv.evaluation.single_table import run_diagnostic
    from sdv.metadata import Metadata
    from sdv.single_table import GaussianCopulaSynthesizer

    metadata = Metadata.load_from_dict(
        {
            "tables": {
                "table": {
                    "columns": {
                        "datetime1": {"sdtype": "datetime"},
                        "datetime2": {"sdtype": "datetime"},
                    }
                }
            }
        }
    )

    data = pd.DataFrame(
        {
            "datetime1": [
                pd.Timestamp("2019-01-01"),
                pd.Timestamp("2019-01-01"),
                pd.Timestamp("2019-12-30"),
            ],
            "datetime2": [pd.Timestamp("2020-01-01")] * 3,
        }
    )

    constraint = Inequality(
        low_column_name="datetime1",
        high_column_name="datetime2",
        table_name="table",
    )

    synthesizer = GaussianCopulaSynthesizer(metadata)
    synthesizer.add_constraints([constraint])
    synthesizer.fit(data)
    sample = synthesizer.sample(500)
    report = run_diagnostic(data, sample, metadata, verbose=False)

    real_min = pd.to_datetime(data["datetime2"]).min()
    real_max = pd.to_datetime(data["datetime2"]).max()
    synth_min = pd.to_datetime(sample["datetime2"]).min()
    synth_max = pd.to_datetime(sample["datetime2"]).max()
    score = report.get_score()
    properties = report.get_properties()

    print("sdv_version=", sdv.__version__)
    print("python_version=", sys.version.replace("\n", " "))
    print("real_datetime2_range=", f"{real_min} -> {real_max}")
    print("sample_datetime2_range=", f"{synth_min} -> {synth_max}")
    print("diagnostic_score=", score)
    print("report_properties=")
    print(properties.to_string(index=False))
    print("reproducible=", score < 1.0)


if __name__ == "__main__":
    main()
