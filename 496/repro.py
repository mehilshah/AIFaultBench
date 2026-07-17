#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RESULT_PATH = ROOT / "reproduction.json"


def _write_result(
    *,
    reproducible: bool,
    evidence: list[str],
    steps: list[str],
    blocking_reason: str | None,
    reproduction_command: str,
) -> None:
    payload = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": steps,
        "blocking_reason": blocking_reason,
        "reproduction_command": reproduction_command,
    }
    RESULT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    os.environ.setdefault("JAX_PLATFORM_NAME", "cpu")
    sys.path.insert(0, str(ROOT / "codebase"))

    import numpy as np
    import jax
    import jax.numpy as jnp

    jax.config.update("jax_enable_x64", True)

    evidence: list[str] = []
    steps: list[str] = []
    blocking_reason: str | None = None
    reproduction_command = "bash run_repro.sh"

    steps.append("Install the pinned JAX runtime and import the local source tree from codebase/.")
    steps.append("Evaluate heaviside for NaN inputs in eager mode and under jax.jit.")

    evidence.append(f"jax version: {jax.__version__}")
    evidence.append(f"jaxlib version: {__import__('jaxlib').__version__}")
    evidence.append(f"numpy version: {np.__version__}")

    cases = [
        (np.float32, np.float32(-1.0)),
        (np.float64, np.float64(-1.0)),
    ]

    mismatches: list[str] = []
    for dtype, x2 in cases:
        x1 = dtype(np.nan)
        np_out = np.heaviside(x1, x2)
        eager_out = jnp.heaviside(jnp.array(x1), jnp.array(x2))
        jit_out = jax.jit(jnp.heaviside)(jnp.array(x1), jnp.array(x2))

        evidence.append(
            f"{dtype.__name__}: numpy={np_out!r}, eager={eager_out!r}, jit={jit_out!r}"
        )
        np_arr = np.asarray(np_out)
        eager_arr = np.asarray(eager_out)
        jit_arr = np.asarray(jit_out)
        if not (
            np.array_equal(np_arr, eager_arr, equal_nan=True)
            and np.array_equal(np_arr, jit_arr, equal_nan=True)
        ):
            mismatches.append(dtype.__name__)

    reproducible = bool(mismatches)
    if reproducible:
        steps.append(
            "Observed a mismatch for both float32 and float64: NumPy returns nan, JAX returns -1.0."
        )
    else:
        blocking_reason = "The reported heaviside NaN mismatch did not reproduce in this environment."
        steps.append("No mismatch was observed for the tested dtypes.")

    _write_result(
        reproducible=reproducible,
        evidence=evidence,
        steps=steps,
        blocking_reason=blocking_reason,
        reproduction_command=reproduction_command,
    )

    print("reproducible:", reproducible)
    for line in evidence:
        print(line)

    return 0 if reproducible else 1


if __name__ == "__main__":
    raise SystemExit(main())
