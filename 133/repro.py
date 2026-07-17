#!/usr/bin/env python3
"""Minimal local reproduction for newline loss in Flair span text."""

from __future__ import annotations

import importlib.util
import pathlib
import sys
import types

import torch


ROOT = pathlib.Path(__file__).resolve().parent
FLAIR_ROOT = ROOT / "codebase" / "flair"


def _load_module(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _bootstrap_local_flair() -> tuple[type, type]:
    flair_pkg = types.ModuleType("flair")
    flair_pkg.__path__ = [str(FLAIR_ROOT)]  # type: ignore[attr-defined]
    flair_pkg._arrow = " -> "
    flair_pkg.device = torch.device("cpu")
    sys.modules["flair"] = flair_pkg

    file_utils = types.ModuleType("flair.file_utils")

    class _Tqdm:
        def __init__(self, iterable, *args, **kwargs):
            self.iterable = iterable

        def __iter__(self):
            return iter(self.iterable)

        def __len__(self):
            return len(self.iterable)

    file_utils.Tqdm = _Tqdm
    sys.modules["flair.file_utils"] = file_utils

    _load_module("flair.tokenization", FLAIR_ROOT / "tokenization.py")
    data_mod = _load_module("flair.data", FLAIR_ROOT / "data.py")

    return data_mod.Sentence, data_mod.Span


def main() -> None:
    Sentence, _Span = _bootstrap_local_flair()

    example = "I am a student named John\nSmith."
    sentence = Sentence(example)

    # The entity spans the newline between "John" and "Smith".
    span = sentence[5:7]
    span.add_label("ner", "PER")
    entity = sentence.get_spans("ner")[0]

    print(sentence)
    print(f"Source Text: {repr(example)}")
    print(f"Entity Start: {entity.start_position}")
    print(f"Entity End: {entity.end_position}")
    print(f"Entity Text: {entity.text}")
    print(f"Entity in source text: {repr(example[entity.start_position:entity.end_position])}")
    assert example[entity.start_position : entity.end_position] == entity.text


if __name__ == "__main__":
    main()
