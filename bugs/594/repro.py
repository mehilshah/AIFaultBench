from __future__ import annotations

from pathlib import Path
import inspect
import sys


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

import jax.numpy as jnp  # noqa: E402


def main() -> None:
    doc = inspect.getdoc(jnp.dot) or ""
    bad_line = (
        "In the multi-dimensional case, leading dimensions must be "
        "broadcast-compatible"
    )
    a = jnp.zeros((3, 4, 2))
    b = jnp.zeros((26, 2, 1))
    out = jnp.dot(a, b)

    print("doc_contains_misleading_line", bad_line in doc)
    print("dot_shape", out.shape)
    print("expected_shape_from_report", (3, 4, 26, 1))
    print("shape_matches_report", tuple(out.shape) == (3, 4, 26, 1))


if __name__ == "__main__":
    main()
