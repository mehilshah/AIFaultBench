#!/usr/bin/env python3
"""Minimal reproduction for the TextPairRegressor state-dict constructor mismatch."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

from flair.data import Sentence  # noqa: E402
from flair.embeddings import DocumentTFIDFEmbeddings  # noqa: E402
from flair.models import TextPairRegressor  # noqa: E402


def main() -> int:
    train = [Sentence("hello world"), Sentence("goodbye world")]
    embeddings = DocumentTFIDFEmbeddings(train)
    model = TextPairRegressor(embeddings, label_type="test")

    state = model._get_state_dict()
    print("state keys:", sorted(state))
    print("document_embeddings saved as:", type(state["document_embeddings"]).__name__)

    try:
        model._init_model_with_state_dict(state)
    except TypeError as exc:
        print("reproduced TypeError:", exc)
        if "document_embeddings" not in str(exc):
            print("unexpected TypeError shape", file=sys.stderr)
            return 2
        return 0

    print("bug not reproduced: model reloaded successfully")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
