#!/usr/bin/env python3
"""Minimal repro for MMS TTS Japanese text being fully filtered as OOV.

This mirrors the `filter_oov()` logic in `codebase/examples/mms/tts/infer.py`
without requiring the missing VITS helper modules or model weights.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VOCAB_PATH = ROOT / "fixtures" / "jvn" / "vocab.txt"


class TextMapper:
    def __init__(self, vocab_file: Path):
        self.symbols = [line.rstrip("\n") for line in vocab_file.read_text(encoding="utf-8").splitlines()]
        self._symbol_to_id = {s: i for i, s in enumerate(self.symbols)}

    def filter_oov(self, text: str) -> str:
        val_chars = self._symbol_to_id
        txt_filt = "".join(list(filter(lambda x: x in val_chars, text)))
        print(f"text after filtering OOV: {txt_filt}")
        return txt_filt


def main() -> int:
    mapper = TextMapper(VOCAB_PATH)

    # Japanese-script input. The bundled MMS Japanese vocab only contains Latin
    # letters, digits, and a few punctuation marks, so this is filtered to "".
    input_text = "これは日本語の再現テストです。"
    filtered = mapper.filter_oov(input_text.lower())
    sequence_length = len(filtered)

    result = {
        "reproducible": filtered == "",
        "input_text": input_text,
        "filtered_text": filtered,
        "filtered_length": sequence_length,
        "evidence": [
            "The MMS Japanese vocab in jvn.tar.gz does not contain Japanese characters.",
            "filter_oov() prints an empty string for Japanese-script input.",
            "The filtered text length is 0, so downstream inference would receive empty text.",
        ],
    }

    (ROOT / "reproduction.json").write_text(json.dumps(
        {
            "reproducible": result["reproducible"],
            "evidence": result["evidence"],
            "steps": [
                "Inspect examples/mms/tts/infer.py and note the filter_oov() print.",
                "Use the official MMS Japanese vocab extracted from jvn.tar.gz.",
                "Run the same OOV filtering on Japanese-script input.",
            ],
            "blocking_reason": "",
            "reproduction_command": "bash run_repro.sh",
        },
        indent=2,
        ensure_ascii=False,
    ) + "\n", encoding="utf-8")

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
