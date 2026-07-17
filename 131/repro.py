#!/usr/bin/env python3
"""Minimal repro for Flair TextRegressor ignoring label_name during training loss."""

import os

os.environ.setdefault("FLAIR_DEVICE", "cpu")

import torch

from flair.data import Sentence
from flair.embeddings.base import DocumentEmbeddings
from flair.models import TextRegressor


class TinyDocEmbeddings(DocumentEmbeddings):
    """Small, deterministic embedding module that avoids any external downloads."""

    def __init__(self) -> None:
        super().__init__()
        self.name = "tiny_doc"
        self._embedding_length = 1

    @property
    def embedding_length(self) -> int:
        return self._embedding_length

    def _add_embeddings_internal(self, sentences):
        for sentence in sentences:
            sentence.set_embedding(self.name, torch.ones(self.embedding_length))

    def to_params(self):
        return {"embedding_length": self._embedding_length}

    @classmethod
    def from_params(cls, params):
        return cls()


def main() -> None:
    sentence = Sentence("This is a sentence")
    sentence.add_label("regression_label", 4.5)
    sentence.add_label("foo", "bar")

    print("sentence labels:", [(label.value, label.score) for label in sentence.labels])
    print(
        "regression labels:",
        [(label.value, label.score) for label in sentence.get_labels("regression_label")],
    )

    model = TextRegressor(TinyDocEmbeddings(), label_name="regression_label")
    model.forward_loss([sentence])


if __name__ == "__main__":
    main()
