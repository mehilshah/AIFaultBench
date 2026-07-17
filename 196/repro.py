from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = str(ROOT / "codebase")

DATACLASS_SNIPPET = r"""
import sys
sys.path.insert(0, {codebase!r})

import chex
import jax.numpy as jnp
from beartype import beartype
from jaxtyping import Float, Array, jaxtyped


@jaxtyped(typechecker=beartype)
@chex.dataclass
class Vector:
    x: Float[Array, "B"]
    y: Float[Array, "B"]


@jaxtyped(typechecker=beartype)
def test(v: Vector) -> Vector:
    return Vector(
        x=v.x[:2],
        y=v.y[:2],
    )


a = Vector(
    x=jnp.arange(10.0),
    y=jnp.arange(10.0),
)
try:
    out = test(a)
except Exception as exc:
    print(f"DATACLASS_CASE=ERROR:{{type(exc).__name__}}:{{exc}}")
else:
    print(f"DATACLASS_CASE=NO_ERROR:{{out}}")
"""

PLAIN_SNIPPET = r"""
import sys
sys.path.insert(0, {codebase!r})

import jax.numpy as jnp
from beartype import beartype
from jaxtyping import Float, Array, jaxtyped


@jaxtyped(typechecker=beartype)
def test(
    x: Float[Array, "B"],
    y: Float[Array, "B"],
) -> tuple[Float[Array, "B"], Float[Array, "B"]]:
    return (x[:2], y[:2])


try:
    test(
        x=jnp.arange(10.0),
        y=jnp.arange(10.0),
    )
except Exception as exc:
    print(f"PLAIN_CASE=ERROR:{{type(exc).__name__}}:{{exc}}")
else:
    print("PLAIN_CASE=NO_ERROR")
"""


def run_snippet(name: str, snippet: str) -> subprocess.CompletedProcess[str]:
    code = "from pathlib import Path\n" + snippet.format(codebase=CODEBASE)
    return subprocess.run(
        [sys.executable, "-c", code],
        check=True,
        capture_output=True,
        text=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=("dataclass", "plain"))
    args = parser.parse_args()

    cases = (
        ("dataclass", DATACLASS_SNIPPET),
        ("plain", PLAIN_SNIPPET),
    )

    if args.case is not None:
        for case_name, snippet in cases:
            if case_name == args.case:
                completed = run_snippet(case_name, snippet)
                if completed.stdout:
                    print(completed.stdout, end="")
                if completed.stderr:
                    print(completed.stderr, end="", file=sys.stderr)
                return
        raise ValueError(args.case)

    for case_name, snippet in cases:
        completed = run_snippet(case_name, snippet)
        if completed.stdout:
            print(completed.stdout, end="")
        if completed.stderr:
            print(completed.stderr, end="", file=sys.stderr)


if __name__ == "__main__":
    main()
