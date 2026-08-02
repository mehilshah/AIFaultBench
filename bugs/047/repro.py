#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "fixtures"


def reorder_decode(hypos: list[str]) -> list[tuple[int, str]]:
    outputs: list[tuple[int, str]] = []
    for hypo in hypos:
        idx = int(re.findall(r"\(None-(\d+)\)$", hypo)[0])
        hypo = re.sub(r"\(\S+\)$", "", hypo).strip()
        outputs.append((idx, hypo))
    return sorted(outputs)


def load_lines(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]


def main() -> int:
    audio_paths = load_lines(FIXTURES / "audio_paths.txt")
    hypo_lines = load_lines(FIXTURES / "hypo.word")
    expected_lines = load_lines(FIXTURES / "expected_transcripts.txt")

    reordered = reorder_decode(hypo_lines)
    observed_lines = [hypo for _, hypo in reordered]

    print("Using the exact reorder logic from examples/mms/asr/infer/mms_infer.py")
    print(f"Audio inputs: {len(audio_paths)}")
    print(f"Hypothesis lines: {len(hypo_lines)}")
    print()

    mismatches: list[dict[str, object]] = []
    for idx, (audio, expected, observed) in enumerate(
        zip(audio_paths, expected_lines, observed_lines)
    ):
        match = expected == observed
        status = "MATCH" if match else "MISMATCH"
        print(f"{idx:02d} {audio}")
        print(f"   expected: {expected}")
        print(f"   observed: {observed}")
        print(f"   status: {status}")
        if not match:
            mismatches.append(
                {
                    "index": idx,
                    "audio": audio,
                    "expected": expected,
                    "observed": observed,
                }
            )

    reproducible = bool(mismatches)
    print()
    print(f"reproducible: {str(reproducible).lower()}")
    if reproducible:
        print(
            "The wrapper preserves the wrong transcript order from hypo.word, "
            "so the logged Input/Output pairing is incorrect."
        )

    result = {
        "reproducible": reproducible,
        "mismatches": mismatches,
        "reordered_indices": [idx for idx, _ in reordered],
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
