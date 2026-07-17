#!/usr/bin/env python3
"""Reproduce the MixupAndCutmix beta sampling bug.

The buggy source is in:
  codebase/official/vision/ops/augment.py
  MixupAndCutmix._sample_from_beta
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import tensorflow as tf


ROOT = Path(__file__).resolve().parent
BUG_SOURCE = ROOT / "codebase" / "official" / "vision" / "ops" / "augment.py"


def buggy_sample_from_beta(alpha: float, beta: float, shape: tuple[int, ...]) -> tf.Tensor:
    """Exact buggy implementation from the local source tree."""
    sample_alpha = tf.random.gamma(shape, 1.0, beta=alpha)
    sample_beta = tf.random.gamma(shape, 1.0, beta=beta)
    return sample_alpha / (sample_alpha + sample_beta)


def summarize(values: np.ndarray) -> dict[str, float]:
    return {
        "mean": float(values.mean()),
        "var": float(values.var()),
        "q10": float(np.quantile(values, 0.10)),
        "q90": float(np.quantile(values, 0.90)),
        "middle_mass": float(((values >= 0.25) & (values <= 0.75)).mean()),
    }


def main() -> int:
    source = BUG_SOURCE.read_text(encoding="utf-8")
    markers = [
        "sample_alpha = tf.random.gamma(shape, 1., beta=alpha)",
        "sample_beta = tf.random.gamma(shape, 1., beta=beta)",
    ]
    missing = [marker for marker in markers if marker not in source]
    if missing:
        raise RuntimeError(
            "Buggy implementation markers not found in local source: "
            + ", ".join(missing)
        )

    alpha = 0.2
    sample_count = 100_000
    sample_shape = (sample_count,)

    tf.random.set_seed(1234)
    np.random.seed(1234)

    buggy = buggy_sample_from_beta(alpha, alpha, sample_shape).numpy()
    beta_ref = np.random.beta(alpha, alpha, sample_count)
    uniform_ref = np.random.uniform(0.0, 1.0, sample_count)

    buggy_stats = summarize(buggy)
    beta_stats = summarize(beta_ref)
    uniform_stats = summarize(uniform_ref)

    evidence = {
        "source": str(BUG_SOURCE),
        "alpha": alpha,
        "samples": sample_count,
        "buggy": buggy_stats,
        "beta_reference": beta_stats,
        "uniform_reference": uniform_stats,
        "buggy_minus_uniform_var": float(
            abs(buggy_stats["var"] - uniform_stats["var"])
        ),
        "buggy_minus_beta_var": float(
            abs(buggy_stats["var"] - beta_stats["var"])
        ),
    }

    # The broken implementation samples from Beta(1, 1) in practice, not
    # Beta(alpha, alpha). For alpha=0.2 this makes the middle of the interval
    # far too dense.
    assert evidence["buggy_minus_uniform_var"] < 0.01, evidence
    assert buggy_stats["var"] < beta_stats["var"] * 0.6, evidence
    assert buggy_stats["middle_mass"] > beta_stats["middle_mass"] + 0.20, evidence

    print(json.dumps(evidence, indent=2, sort_keys=True))
    print(
        "Result: reproducible. The local sampler behaves like a near-uniform "
        "Beta(1, 1) draw instead of Beta(0.2, 0.2)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
