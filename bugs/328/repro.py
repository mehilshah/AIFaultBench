#!/usr/bin/env python3
"""Reproduce POT issue 24.

The reported behavior is that OTDA produces a transport matrix whose total mass
is below 1.0 when fitting on two random point clouds.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
sys.path.insert(0, str(CODEBASE))

from compat_shims import apply as apply_compat_shims

apply_compat_shims()

import numpy as np
import ot


def main() -> int:
    np.random.seed(0)

    a = np.random.rand(1500, 95)
    b = np.random.rand(50000, 95)

    opt = ot.da.OTDA()
    opt.fit(a, b)

    total_mass = float(np.sum(opt.G))
    print(f"ot_version={ot.__version__}")
    print(f"sum(opt.G)={total_mass:.16f}")
    print("expected=1.0")

    if np.isclose(total_mass, 1.0, rtol=1e-3, atol=1e-3):
        print("result=not_reproduced")
        return 0

    print("result=reproduced")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
