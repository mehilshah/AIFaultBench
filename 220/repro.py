#!/usr/bin/env python3
"""Deterministic reproducer for the plant_leaves checksum failure.

The live upstream URL from the report currently returns HTTP 403, so this
script demonstrates the exact TFDS checksum validation failure locally by
feeding the reported expected checksum a tiny archive with different bytes.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
CHECKSUMS_PATH = (
    CODEBASE / "tensorflow_datasets" / "datasets" / "plant_leaves" / "checksums.tsv"
)
REPORTED_URL = (
    "https://prod-dcd-datasets-cache-zipfiles.s3.eu-west-1.amazonaws.com/"
    "hb74ynkjcn-1.zip"
)

sys.path.insert(0, str(CODEBASE))

from tensorflow_datasets.core.download import checksums  # noqa: E402
from tensorflow_datasets.core.download import download_manager  # noqa: E402


def _build_tiny_zip(path: Path) -> None:
  path.write_bytes(b"local placeholder data")


def main() -> int:
  expected = checksums.load_url_infos(CHECKSUMS_PATH)[REPORTED_URL]

  with tempfile.TemporaryDirectory(prefix="plant_leaves_repro_") as tmp:
    archive_path = Path(tmp) / "hb74ynkjcn-1.zip"
    _build_tiny_zip(archive_path)
    actual = checksums.compute_url_info(archive_path)

    print(f"expected_checksum={expected.checksum}")
    print(f"actual_checksum={actual.checksum}")
    print(f"actual_size={int(actual.size)}")

    try:
      live = requests.get(REPORTED_URL, stream=True, timeout=20)
      print(f"live_url_status={live.status_code}")
      live.close()
    except Exception as exc:  # pragma: no cover - network dependent
      print(f"live_url_error={type(exc).__name__}: {exc}")

    try:
      download_manager._validate_checksums(  # pylint: disable=protected-access
          url=REPORTED_URL,
          path=archive_path,
          computed_url_info=actual,
          expected_url_info=expected,
          force_checksums_validation=False,
      )
      print("unexpected_result=no_error")
      return 1
    except download_manager.NonMatchingChecksumError as exc:
      print("result=NonMatchingChecksumError")
      print(exc)
      return 0


if __name__ == "__main__":
  raise SystemExit(main())
