#!/usr/bin/env python3
from __future__ import annotations

import os
import sys

os.environ.setdefault("KERAS_BACKEND", "numpy")

import numpy as np
import keras

import bayesflow as bf


def main() -> int:
    seed = 0
    np.random.seed(seed)
    keras.utils.set_random_seed(seed)

    network = bf.networks.PointInferenceNetwork(scores=dict(mvn=bf.scores.MultivariateNormalScore()))

    xz = keras.ops.convert_to_tensor(np.random.normal(0, 1, size=(64, 3)))
    conditions = keras.ops.convert_to_tensor(np.random.normal(0, 10, size=(64, 2)))

    covariance = network(xz=xz, conditions=conditions)["mvn"]["covariance"]
    inverse = keras.ops.inv(covariance)
    inverse_np = np.array(inverse)
    covariance_np = np.array(covariance)

    inverse_finite = bool(np.isfinite(inverse_np).all())

    print(f"backend={keras.backend.backend()}")
    print(f"seed={seed}")
    print(f"covariance_shape={covariance_np.shape}")
    print(f"covariance_finite={bool(np.isfinite(covariance_np).all())}")
    print(f"inverse_finite={inverse_finite}")
    print(f"inverse_has_inf={bool(np.isinf(inverse_np).any())}")
    print(f"inverse_has_nan={bool(np.isnan(inverse_np).any())}")
    print(f"inverse_min={np.nanmin(inverse_np)}")
    print(f"inverse_max={np.nanmax(inverse_np)}")

    if not inverse_finite:
        print("bug_reproduced=non_finite_inverse")
        return 1

    print("bug_reproduced=not_observed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
