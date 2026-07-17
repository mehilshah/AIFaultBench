import os
import sys

import numpy as np


def main() -> int:
    sys.path.insert(0, os.path.abspath("codebase"))

    import ot

    sample1 = np.array([0.1, 0.11, 0.4, 0.6])
    sample2 = np.array([0.21, 0.15, 0.7, 0.95])
    delta = 0.02

    d1 = ot.wasserstein_circle(sample1, sample2)
    d2 = ot.wasserstein_circle(sample1 + delta, sample2 + delta)
    d2_mod = ot.wasserstein_circle((sample1 + delta) % 1, (sample2 + delta) % 1)
    d2_p2 = ot.wasserstein_circle(sample1 + delta, sample2 + delta, p=2)
    d1_p2 = ot.wasserstein_circle(sample1, sample2, p=2)

    print("POT wasserstein_circle repro")
    print(f"sample1={sample1.tolist()}")
    print(f"sample2={sample2.tolist()}")
    print(f"delta={delta}")
    print(f"d1_p1={d1.tolist()}")
    print(f"d2_p1={d2.tolist()}")
    print(f"d2_mod_p1={d2_mod.tolist()}")
    print(f"d1_p2={d1_p2.tolist()}")
    print(f"d2_p2={d2_p2.tolist()}")
    print(f"p1_equal={bool(np.array_equal(d1, d2))}")
    print(f"p1_allclose={bool(np.allclose(d1, d2))}")
    print(f"p2_allclose={bool(np.allclose(d1_p2, d2_p2))}")

    if np.array_equal(d1, d2):
        print("Unexpected: p=1 values are exactly equal.")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
