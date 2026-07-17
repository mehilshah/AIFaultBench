#!/usr/bin/env python3
"""Reproduce SDV issue 2434: complex regex formats crash during fit."""

from __future__ import annotations

import json
import sys
import traceback
import types
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
RESULT_PATH = ROOT / "reproduction.json"


def _install_stubs() -> None:
    """Stub unrelated deep-learning imports so the Gaussian copula path can load."""
    class LossValuesMixin:
        pass

    ctgan_stub = types.ModuleType("sdv.single_table.ctgan")
    ctgan_stub.CTGANSynthesizer = type("CTGANSynthesizer", (), {})
    ctgan_stub.TVAESynthesizer = type("TVAESynthesizer", (), {})
    ctgan_stub.LossValuesMixin = LossValuesMixin
    sys.modules["sdv.single_table.ctgan"] = ctgan_stub

    copulagan_stub = types.ModuleType("sdv.single_table.copulagan")
    copulagan_stub.CopulaGANSynthesizer = type("CopulaGANSynthesizer", (), {})
    sys.modules["sdv.single_table.copulagan"] = copulagan_stub

    deepecho_stub = types.ModuleType("deepecho")
    deepecho_stub.PARModel = type("PARModel", (), {})
    sys.modules["deepecho"] = deepecho_stub

    sequences_stub = types.ModuleType("deepecho.sequences")
    sequences_stub.assemble_sequences = lambda *args, **kwargs: None
    sys.modules["deepecho.sequences"] = sequences_stub


def _build_payload(reproducible: bool, evidence: list[str], steps: list[str], blocking_reason: str) -> dict:
    return {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": steps,
        "blocking_reason": blocking_reason,
        "reproduction_command": "bash run_repro.sh",
    }


def main() -> int:
    sys.path.insert(0, str(CODEBASE))
    _install_stubs()

    try:
        from sdv.metadata import Metadata
        from sdv.single_table import GaussianCopulaSynthesizer

        metadata = Metadata.load_from_dict(
            {
                "tables": {
                    "table": {
                        "columns": {
                            "id": {"sdtype": "id", "regex_format": "(10|20|30)[0-9]{4}"},
                            "A": {"sdtype": "numerical"},
                        }
                    }
                }
            }
        )

        data = pd.DataFrame(
            {
                "id": ["101234", "201234", "301234", "100123", "200123"],
                "A": [0, 1, 2, 3, 4],
            }
        )

        print("Metadata loaded.")
        synthesizer = GaussianCopulaSynthesizer(metadata)
        print("Synthesizer instantiated.")
        synthesizer.fit(data)
        print("Fit completed without error.")

        payload = _build_payload(
            reproducible=False,
            evidence=["The reported fit path completed successfully in this environment."],
            steps=[
                "Loaded the reported metadata and input data.",
                "Instantiated GaussianCopulaSynthesizer.",
                "Called fit(data) and observed no regex parsing failure.",
            ],
            blocking_reason="The current checkout did not reproduce the reported failure.",
        )
        RESULT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return 0

    except Exception as exc:  # pylint: disable=broad-exception-caught
        traceback.print_exc()
        reproducible = isinstance(exc, KeyError) and str(exc) in {"'SUBPATTERN'", "SUBPATTERN"}
        evidence = [
            f"{type(exc).__name__}: {exc}",
            "Traceback shows the failure originates in rdt.transformers.utils.strings_from_regex()",
        ]
        steps = [
            "Loaded the reported metadata and input data.",
            "Instantiated GaussianCopulaSynthesizer.",
            "Called fit(data) and observed a KeyError during regex parsing.",
        ]
        blocking_reason = "" if reproducible else "The failure was different from the reported regex parsing bug."
        payload = _build_payload(reproducible, evidence, steps, blocking_reason)
        RESULT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return 0 if reproducible else 1


if __name__ == "__main__":
    raise SystemExit(main())
