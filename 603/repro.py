#!/usr/bin/env python3
"""Synthetic reproduction for NumPyro issue 2008.

This keeps the model structure from the bug report:
- a Python loop over classrooms
- `solve_classroom_equilibrium` inside the model
- repeated `SVI.update` calls with `Trace_ELBO`

The original report used a parquet file that is not part of the benchmark
folder, so this script generates a small synthetic dataset with variable
classroom sizes to exercise the same execution path.
"""

from __future__ import annotations

import argparse
import os
from functools import partial

import jax
import jax.numpy as jnp
import numpyro
import numpyro.distributions as dist
import psutil
from numpyro.distributions import constraints
from numpyro.infer import SVI, Trace_ELBO
from numpyro.optim import Adam


def solve_classroom_equilibrium(x_c, alpha_c, beta, gamma, max_iter=20):
    n_students = x_c.shape[0]
    p = jnp.full((n_students,), 0.5)

    def body_fn(_, p_curr):
        pbar = p_curr.mean()
        logits = alpha_c + jnp.dot(x_c, beta) + gamma * pbar
        return jax.nn.sigmoid(logits)

    return jax.lax.fori_loop(0, max_iter, body_fn, p)


def structural_model(classroom_list):
    beta = numpyro.sample("beta", dist.Normal(0.0, 1.0).expand([3]))
    gamma = numpyro.sample("gamma", dist.Normal(0.0, 1.0))
    fe_offset = numpyro.sample("fe_offset", dist.Normal(-2.0, 1.0))

    total_loglike = 0.0
    for _, x_c, _, y_c in classroom_list:
        p_c = solve_classroom_equilibrium(x_c, fe_offset, beta, gamma, max_iter=20)
        total_loglike = total_loglike + jnp.sum(dist.Bernoulli(probs=p_c).log_prob(y_c))

    numpyro.factor("likelihood", total_loglike)


def structural_guide(classroom_list):
    dim_bg = 5
    loc_bg = numpyro.param("loc_bg", jnp.zeros(dim_bg))
    l_unconstrained = numpyro.param(
        "L_bg_unconstrained",
        jnp.eye(dim_bg) * 0.1,
        constraint=constraints.lower_cholesky,
    )
    l_bg = jnp.tril(l_unconstrained)
    z_bg = numpyro.sample(
        "_beta_gamma",
        dist.MultivariateNormal(loc=loc_bg, scale_tril=l_bg),
        infer={"is_auxiliary": True},
    )

    numpyro.sample("beta", dist.Delta(z_bg[:3]))
    numpyro.sample("gamma", dist.Delta(z_bg[3]))
    numpyro.sample("fe_offset", dist.Delta(z_bg[4]))


def make_synthetic_classrooms(num_classrooms: int):
    classroom_list = []
    for c_id in range(num_classrooms):
        n_students = 3 + (c_id % 5)
        x_c = jnp.arange(n_students * 3, dtype=jnp.float32).reshape(n_students, 3)
        x_c = x_c / 10.0 + c_id * 0.1
        s_c = jnp.zeros((n_students,), dtype=jnp.int32)
        y_c = (jnp.arange(n_students) % 2).astype(jnp.int32)
        classroom_list.append((c_id, x_c, s_c, y_c))
    return classroom_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--classrooms", type=int, default=12)
    parser.add_argument("--iters", type=int, default=10)
    args = parser.parse_args()

    numpyro.enable_validation(True)
    jax.config.update("jax_enable_x64", False)

    classroom_list = make_synthetic_classrooms(args.classrooms)
    svi = SVI(
        partial(structural_model, classroom_list),
        partial(structural_guide, classroom_list),
        Adam(1e-2),
        Trace_ELBO(),
    )

    state = svi.init(jax.random.PRNGKey(0))
    proc = psutil.Process(os.getpid())
    rss0 = proc.memory_info().rss / 1024**2
    print(f"initial_rss_mb={rss0:.2f}")

    losses = []
    rss_values = [rss0]
    for i in range(args.iters):
        state, loss = svi.update(state)
        loss_value = float(loss)
        rss_mb = proc.memory_info().rss / 1024**2
        losses.append(loss_value)
        rss_values.append(rss_mb)
        print(f"iter={i} loss={loss_value:.4f} rss_mb={rss_mb:.2f}")

    print(
        "summary "
        f"loss_start={losses[0]:.4f} loss_end={losses[-1]:.4f} "
        f"rss_start={rss_values[0]:.2f} rss_end={rss_values[-1]:.2f} "
        f"rss_delta={rss_values[-1] - rss_values[0]:.2f}"
    )


if __name__ == "__main__":
    main()
