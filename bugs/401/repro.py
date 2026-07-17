#!/usr/bin/env python3
import argparse

import torch

import pyro
import pyro.distributions as dist
from pyro.contrib.cevae import CEVAE


def generate_data(num_data, feature_dim):
    z = dist.Bernoulli(0.5).sample([num_data])
    x = dist.Normal(z, 5 * z + 3 * (1 - z)).sample([feature_dim]).t()
    t = dist.Bernoulli(0.75 * z + 0.25 * (1 - z)).sample()
    y = dist.Bernoulli(logits=3 * (z + 2 * (2 * t - 2))).sample()
    return x, t, y


def main():
    parser = argparse.ArgumentParser(description="Reproduce CEVAE CUDA bug")
    parser.add_argument("--num-data", type=int, default=10)
    parser.add_argument("--feature-dim", type=int, default=5)
    parser.add_argument("--latent-dim", type=int, default=20)
    parser.add_argument("--hidden-dim", type=int, default=200)
    parser.add_argument("--num-layers", type=int, default=3)
    parser.add_argument("--num-epochs", type=int, default=1)
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--seed", type=int, default=1234567890)
    parser.add_argument("--cuda", action="store_true")
    args = parser.parse_args()

    if args.cuda:
        torch.set_default_tensor_type("torch.cuda.FloatTensor")

    pyro.set_rng_seed(args.seed)
    x_train, t_train, y_train = generate_data(args.num_data, args.feature_dim)

    pyro.set_rng_seed(args.seed)
    pyro.clear_param_store()
    cevae = CEVAE(
        feature_dim=args.feature_dim,
        latent_dim=args.latent_dim,
        hidden_dim=args.hidden_dim,
        num_layers=args.num_layers,
        num_samples=10,
    )
    cevae.fit(
        x_train,
        t_train,
        y_train,
        num_epochs=args.num_epochs,
        batch_size=args.batch_size,
    )


if __name__ == "__main__":
    assert pyro.__version__.startswith("1.8.6")
    main()
