#!/usr/bin/env python3
"""Reproduce the `output_value=None` prompt bug in SentenceTransformer.encode()."""

from __future__ import annotations

from pathlib import Path
import sys
import traceback

import torch


def build_model():
    repo_root = Path(__file__).resolve().parent
    sys.path.insert(0, str(repo_root / "codebase"))

    from sentence_transformers import SentenceTransformer

    class DummySentenceTransformer(SentenceTransformer):
        def __init__(self) -> None:
            torch.nn.Module.__init__(self)
            self.add_module("identity", torch.nn.Identity())
            self.prompts = {"query": "query: "}
            self.default_prompt_name = "query"
            self.truncate_dim = None
            self.module_kwargs = None
            self.is_hpu_graph_enabled = False

        def tokenize(self, sentences):
            if isinstance(sentences, str):
                sentences = [sentences]

            lengths = [max(1, len(sentence.split()) + 1) for sentence in sentences]
            max_len = max(lengths) if lengths else 1

            input_ids = torch.zeros((len(sentences), max_len), dtype=torch.long)
            attention_mask = torch.zeros((len(sentences), max_len), dtype=torch.long)

            for row, length in enumerate(lengths):
                input_ids[row, :length] = 1
                attention_mask[row, :length] = 1

            return {"input_ids": input_ids, "attention_mask": attention_mask}

        def forward(self, features, **kwargs):
            batch_size, seq_len = features["input_ids"].shape
            hidden_size = 4

            sentence_embedding = torch.arange(batch_size * hidden_size, dtype=torch.float32).reshape(
                batch_size, hidden_size
            )
            token_embeddings = torch.arange(batch_size * seq_len * hidden_size, dtype=torch.float32).reshape(
                batch_size, seq_len, hidden_size
            )

            return {
                "sentence_embedding": sentence_embedding,
                "token_embeddings": token_embeddings,
                "attention_mask": features["attention_mask"],
                "prompt_length": features["prompt_length"],
            }

        def _text_length(self, sentence):
            return len(sentence)

    return DummySentenceTransformer()


def main() -> int:
    model = build_model()

    try:
        model.encode(["sentence1", "sentence2"], output_value=None)
    except TypeError as exc:
        traceback.print_exc()
        if "'int' object is not subscriptable" not in str(exc):
            print(f"Unexpected TypeError: {exc}")
            return 1
        print("BUG_REPRODUCED: encode(..., output_value=None) crashes on prompt_length")
        return 0
    except Exception:
        traceback.print_exc()
        return 1

    print("BUG_NOT_REPRODUCED: encode(..., output_value=None) returned successfully")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
