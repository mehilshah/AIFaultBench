#!/usr/bin/env python3
"""
Minimal repro for stanza issue 1366.

The report iterates over `doc.sentences[i].to_dict()` and indexes `word['xpos']`.
That fails when the list contains a multi-word token dictionary that omits xpos.
This script loads the local Stanza source tree without importing the broken
system `torch`, constructs a sentence containing an MWT, and demonstrates the
KeyError on the same access pattern.
"""

from __future__ import annotations

import importlib.machinery
import pathlib
import sys
import types


def make_package(name: str, path: pathlib.Path) -> types.ModuleType:
    pkg = types.ModuleType(name)
    pkg.__path__ = [str(path)]
    pkg.__package__ = name
    spec = importlib.machinery.ModuleSpec(name, loader=None, is_package=True)
    spec.submodule_search_locations = [str(path)]
    pkg.__spec__ = spec
    sys.modules[name] = pkg
    return pkg


def install_import_shims(codebase: pathlib.Path) -> None:
    # Avoid the broken globally installed torch in this environment.
    torch = types.ModuleType("torch")
    torch.__file__ = "<repro torch stub>"
    sys.modules["torch"] = torch

    # Load the local stanza tree as a package without executing stanza/__init__.py.
    make_package("stanza", codebase / "stanza")


def build_document():
    from stanza.models.common.doc import Document

    text = "My favorite actress is Joanna Lumley."
    sentence = [
        {"id": 1, "text": "My", "lemma": "my", "upos": "PRON", "xpos": "PRP$", "feats": "Poss=Yes|PronType=Prs", "head": 3, "deprel": "det", "start_char": 0, "end_char": 2},
        {"id": 2, "text": "favorite", "lemma": "favorite", "upos": "ADJ", "xpos": "JJ", "feats": "Degree=Pos", "head": 3, "deprel": "amod", "start_char": 3, "end_char": 11},
        {"id": 3, "text": "actress", "lemma": "actress", "upos": "NOUN", "xpos": "NN", "feats": "Number=Sing", "head": 5, "deprel": "nsubj", "start_char": 12, "end_char": 19},
        {"id": 4, "text": "is", "lemma": "be", "upos": "AUX", "xpos": "VBZ", "feats": "Mood=Ind|Tense=Pres|VerbForm=Fin", "head": 5, "deprel": "cop", "start_char": 20, "end_char": 22},
        {"id": (5, 6), "text": "Joanna Lumley", "start_char": 23, "end_char": 36, "misc": "MWT=Yes"},
        {"id": 5, "text": "Joanna", "lemma": "Joanna", "upos": "PROPN", "feats": "Number=Sing", "head": 3, "deprel": "flat", "start_char": 23, "end_char": 29},
        {"id": 6, "text": "Lumley", "lemma": "Lumley", "upos": "PROPN", "xpos": "NNP", "feats": "Number=Sing", "head": 3, "deprel": "flat", "start_char": 30, "end_char": 36},
        {"id": 7, "text": ".", "lemma": ".", "upos": "PUNCT", "xpos": ".", "head": 5, "deprel": "punct", "start_char": 36, "end_char": 37},
    ]
    return Document([sentence], text=text)


def main() -> int:
    repo_root = pathlib.Path(__file__).resolve().parent
    codebase = repo_root / "codebase"
    sys.path.insert(0, str(codebase))
    install_import_shims(codebase)

    doc = build_document()
    sentence_dicts = doc.sentences[0].to_dict()

    print("sentence.to_dict() output:")
    for entry in sentence_dicts:
        print(entry)

    print("\naccessing word['xpos'] for each entry:")
    for entry in sentence_dicts:
        print(f"entry id={entry['id']!r} keys={sorted(entry.keys())}")
        print(entry["xpos"])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
