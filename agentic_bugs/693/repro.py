#!/usr/bin/env python3
"""Reproduce SimplePropertyGraphStore's Windows default-encoding failure."""

from pathlib import Path
from tempfile import TemporaryDirectory

from llama_index.core.graph_stores.simple_labelled import SimplePropertyGraphStore
from llama_index.core.graph_stores.types import EntityNode


class WindowsCp1252FileSystem:
    """Minimal fsspec-compatible file system emulating Windows' cp1252 default."""

    def open(self, path: str, mode: str):
        # The buggy store calls fs.open(path, "w") without encoding="utf-8".
        return open(path, mode, encoding="cp1252")


def main() -> None:
    store = SimplePropertyGraphStore()
    store.upsert_nodes([EntityNode(name="定义")])

    with TemporaryDirectory() as directory:
        persist_path = str(Path(directory) / "property_graph_store.json")
        try:
            store.persist(persist_path, fs=WindowsCp1252FileSystem())
        except UnicodeEncodeError as error:
            assert error.encoding == "charmap", error
            assert "character maps to <undefined>" in str(error), error
            print(f"OBSERVED BUG: {error.__class__.__name__}: {error}")
            raise SystemExit(1)

    raise AssertionError("Expected cp1252 persistence to reject the Chinese graph node")


if __name__ == "__main__":
    main()
