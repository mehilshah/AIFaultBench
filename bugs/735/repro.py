#!/usr/bin/env python3
"""Reproduce FAISS.list's uninitialized-index return-contract violation."""

import tempfile

from mem0.vector_stores.faiss import FAISS


with tempfile.TemporaryDirectory(prefix="mem0-faiss-repro-") as tmpdir:
    store = FAISS(collection_name="t", path=tmpdir, distance_strategy="euclidean")
    store.index = None  # Model a fresh/uninitialized FAISS index.
    result = store.list(filters={"user_id": "alice"})

if result != [[]]:
    print(f"OBSERVED BUG: FAISS.list() returned {result!r}; expected [[]]")
    raise AssertionError("uninitialized FAISS.list() violates its List[List[OutputData]] contract")

print("BUG NOT OBSERVED: FAISS.list() returned the expected nested empty list")
