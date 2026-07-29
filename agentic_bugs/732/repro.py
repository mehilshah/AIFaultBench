#!/usr/bin/env python3
"""Offline reproduction for mem0 issue #6258 at the pinned checkout."""

import importlib.util
import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VECTOR_STORES = ROOT / "codebase" / "mem0" / "vector_stores"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# _generate_where_clause is pure conversion logic.  Stub the optional Chroma
# client import so loading the checkout makes no service or network calls.
chromadb = types.ModuleType("chromadb")
chromadb.Client = type("Client", (), {})
chromadb.Collection = type("Collection", (), {})
config = types.ModuleType("chromadb.config")
config.Settings = type("Settings", (), {})
chromadb.config = config
sys.modules["chromadb"] = chromadb
sys.modules["chromadb.config"] = config

mem0 = types.ModuleType("mem0")
mem0.__path__ = [str(ROOT / "codebase" / "mem0")]
vector_stores = types.ModuleType("mem0.vector_stores")
vector_stores.__path__ = [str(VECTOR_STORES)]
sys.modules["mem0"] = mem0
sys.modules["mem0.vector_stores"] = vector_stores

load_module("mem0.vector_stores.base", VECTOR_STORES / "base.py")
chroma = load_module("mem0.vector_stores.chroma", VECTOR_STORES / "chroma.py")

where = chroma.ChromaDB._generate_where_clause({"age": {"betwen": [10, 20]}})
expected_silent_result = {"age": {"$eq": [10, 20]}}
if where == expected_silent_result:
    print(f"BUG REPRODUCED: unsupported operator 'betwen' silently became {where!r}")
    raise AssertionError("unsupported operator was silently downgraded to equality")

raise AssertionError(f"Expected silent equality downgrade, got {where!r}")
