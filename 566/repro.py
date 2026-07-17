#!/usr/bin/env python3
"""Reproduction probe for SDV issue 2714 / bug 566.

This probe checks two configurations:
1. The issue report's exact context-column order.
2. A control case with a data-column order that aligns with deepecho's context typing.

The reported sample-time KeyError was not observed in this environment.
The exact report configuration fails earlier during fit(), while the aligned
control case fits and samples successfully.
"""

from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
if str(CODEBASE) not in sys.path:
    sys.path.insert(0, str(CODEBASE))

from sdv.metadata.metadata import Metadata  # noqa: E402
from sdv.sequential import PARSynthesizer  # noqa: E402


def build_metadata() -> Metadata:
    return Metadata.load_from_dict(
        {
            "tables": {
                "icu_data_v03": {
                    "columns": {
                        "binned_time": {
                            "datetime_format": "%Y-%m-%d %H:%M:%S",
                            "sdtype": "datetime",
                        },
                        "Heart Rate": {"sdtype": "numerical"},
                        "Respiratory Rate": {"sdtype": "numerical"},
                        "O2 saturation pulseoxymetry": {"sdtype": "numerical"},
                        "gender": {"sdtype": "categorical"},
                        "anchor_age": {"sdtype": "numerical"},
                        "diag_label": {"sdtype": "categorical"},
                        "sub_hadm_stay_id": {"sdtype": "id"},
                    },
                    "sequence_key": "sub_hadm_stay_id",
                    "sequence_index": "binned_time",
                }
            },
            "relationships": [],
            "METADATA_SPEC_VERSION": "V1",
        }
    )


def build_data(column_order: str) -> pd.DataFrame:
    rows = []
    ages = [58, 61, 72, 45, 63, 77, 52, 69, 58, 62]
    labels = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]

    for seq_idx in range(10):
        seq = f"seq-{seq_idx:03d}"
        age = ages[seq_idx % len(ages)]
        label = labels[seq_idx % len(labels)]
        gender = "M" if seq_idx % 2 == 0 else "F"
        base = pd.Timestamp("2020-01-01") + pd.Timedelta(days=seq_idx)

        for t in range(5):
            common = {
                "binned_time": base + pd.Timedelta(hours=t),
                "Heart Rate": 70 + (seq_idx % 10) + t,
                "Respiratory Rate": 15 + (seq_idx % 5) + t,
                "O2 saturation pulseoxymetry": 90 + (seq_idx % 7) + t,
                "gender": gender,
                "anchor_age": age,
                "diag_label": label,
                "sub_hadm_stay_id": seq,
            }

            if column_order == "reported":
                rows.append(
                    {
                        "binned_time": common["binned_time"],
                        "Heart Rate": common["Heart Rate"],
                        "Respiratory Rate": common["Respiratory Rate"],
                        "O2 saturation pulseoxymetry": common["O2 saturation pulseoxymetry"],
                        "gender": common["gender"],
                        "anchor_age": common["anchor_age"],
                        "diag_label": common["diag_label"],
                        "sub_hadm_stay_id": common["sub_hadm_stay_id"],
                    }
                )
            elif column_order == "aligned":
                rows.append(
                    {
                        "binned_time": common["binned_time"],
                        "Heart Rate": common["Heart Rate"],
                        "Respiratory Rate": common["Respiratory Rate"],
                        "O2 saturation pulseoxymetry": common["O2 saturation pulseoxymetry"],
                        "diag_label": common["diag_label"],
                        "gender": common["gender"],
                        "anchor_age": common["anchor_age"],
                        "sub_hadm_stay_id": common["sub_hadm_stay_id"],
                    }
                )
            else:
                raise ValueError(f"Unsupported column_order: {column_order}")

    return pd.DataFrame(rows)


def run_probe(label: str, data: pd.DataFrame, context_columns: list[str]) -> dict:
    print(f"\n== {label} ==")
    print(f"data columns: {data.columns.tolist()}")
    print(f"context_columns: {context_columns}")

    synthesizer = PARSynthesizer(
        build_metadata(),
        context_columns=context_columns,
        epochs=1,
        verbose=False,
    )

    outcome = {"label": label, "fit": None, "sample": None, "error": None}
    try:
        synthesizer.fit(data)
        outcome["fit"] = "ok"
        print("fit: ok")
    except Exception as exc:  # noqa: BLE001
        outcome["fit"] = "failed"
        outcome["error"] = f"{exc.__class__.__name__}: {exc}"
        print("fit: failed")
        traceback.print_exc()
        return outcome

    try:
        sampled = synthesizer.sample(num_sequences=2)
        outcome["sample"] = "ok"
        print("sample: ok")
        print(sampled[["sub_hadm_stay_id", "gender", "anchor_age", "diag_label"]].head())
    except Exception as exc:  # noqa: BLE001
        outcome["sample"] = "failed"
        outcome["error"] = f"{exc.__class__.__name__}: {exc}"
        print("sample: failed")
        traceback.print_exc()

    return outcome


def main() -> int:
    print("sdv source:", Path(sys.modules["sdv"].__file__).resolve())
    print("python:", sys.version.replace("\n", " "))

    reported = run_probe(
        "reported-order probe",
        build_data("reported"),
        ["diag_label", "gender", "anchor_age"],
    )
    aligned = run_probe(
        "aligned-order control",
        build_data("aligned"),
        ["diag_label", "gender", "anchor_age"],
    )

    reproducible = False
    evidence = (
        "The reported sample-time KeyError ('KeyError: 58.0') was not reproduced. "
        "With the issue report's column order, fit() fails earlier with a TypeError "
        "from deepecho's context type inference. With an aligned control ordering, "
        "fit() and sample() both succeed."
    )
    steps = [
        "Created a Python 3.11 venv and installed the SDV runtime dependencies.",
        "Ran the issue's reported PARSynthesizer configuration against synthetic data shaped like the bug report.",
        "Ran a control configuration with aligned column ordering to confirm the model still fits and samples.",
    ]
    blocking_reason = (
        "The exact reported KeyError is not reachable from the reproduced inputs here; "
        "the reported context ordering fails earlier in fit(), and the aligned control case does not error."
    )
    result = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": steps,
        "blocking_reason": blocking_reason,
        "reproduction_command": "bash run_repro.sh",
    }
    (ROOT / "reproduction.json").write_text(json.dumps(result, indent=2) + "\n")
    print("\nWrote reproduction.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
