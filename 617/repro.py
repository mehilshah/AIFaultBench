import traceback

import torch

import pyro.distributions as dist


def main():
    mean = torch.zeros((0,)).unsqueeze(0)
    covariance = torch.eye(0).unsqueeze(0).repeat(3, 1, 1)

    print(f"mean.shape = {tuple(mean.shape)}")
    print(f"covariance.shape = {tuple(covariance.shape)}")
    print("constructing dist.MultivariateNormal(...)")
    try:
        dist.MultivariateNormal(mean, covariance)
    except Exception as exc:
        print(f"{type(exc).__name__}: {exc}")
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
