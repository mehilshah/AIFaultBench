#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "codebase"))

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402


def probe(enable_x64: bool) -> dict[str, object]:
  jax.config.update("jax_enable_x64", enable_x64)

  a = np.array([1, 3, 5, 7, 9, 11], dtype=np.int32)
  vals = np.array([1, 5, 11], dtype=np.int32)
  np_out = np.searchsorted(a, vals)
  jnp_out = jnp.searchsorted(jnp.array(a), jnp.array(vals))

  return {
      "jax_enable_x64": enable_x64,
      "numpy_dtype": str(np_out.dtype),
      "jax_dtype": str(jnp_out.dtype),
      "jax_values": np.asarray(jnp_out).tolist(),
      "numpy_values": np_out.tolist(),
  }


def main() -> int:
  results = [probe(False), probe(True)]
  print(json.dumps(results, indent=2))

  repro = all(row["numpy_dtype"] == "int64" for row in results) and all(
      row["jax_dtype"] == "int32" for row in results
  )
  print(
      "BUG REPRODUCED" if repro else "BUG NOT REPRODUCED",
      "- jnp.searchsorted ignores jax_enable_x64 for dtype selection",
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
