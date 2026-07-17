#!/usr/bin/env python3
from __future__ import annotations

import json

import numpy as np

from local_ot_loader import load_local_sinkhorn_knopp_unbalanced


def main() -> None:
    sinkhorn_knopp_unbalanced = load_local_sinkhorn_knopp_unbalanced()

    a = np.array([0.5, 0.5])
    b = np.array([0.5, 0.5])
    M = np.array([[0.0, 1.0], [1.0, 0.0]])
    plan = sinkhorn_knopp_unbalanced(a, b, M, 1.0, 1.0)

    expected_094 = np.array([[0.51122814, 0.18807032], [0.18807032, 0.51122814]])
    expected_095 = np.array([[0.32205361, 0.1184769], [0.1184769, 0.32205361]])

    print("input_a =", a.tolist())
    print("input_b =", b.tolist())
    print("cost_matrix =", M.tolist())
    print("observed_plan =")
    print(np.array2string(np.asarray(plan), precision=8))
    print("matches_pot_0_9_4 =", bool(np.allclose(plan, expected_094, atol=1e-8)))
    print("matches_pot_0_9_5 =", bool(np.allclose(plan, expected_095, atol=1e-8)))
    print(
        "max_abs_diff_vs_0_9_4 =",
        float(np.max(np.abs(np.asarray(plan) - expected_094))),
    )
    print(
        "max_abs_diff_vs_0_9_5 =",
        float(np.max(np.abs(np.asarray(plan) - expected_095))),
    )

    print(
        json.dumps(
            {
                "plan": np.asarray(plan).tolist(),
                "matches_pot_0_9_4": bool(np.allclose(plan, expected_094, atol=1e-8)),
                "matches_pot_0_9_5": bool(np.allclose(plan, expected_095, atol=1e-8)),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
