import math
import sys

import torch
import gpytorch


def main() -> None:
    torch.manual_seed(0)
    print(f"torch={torch.__version__}", flush=True)
    print("building training data", flush=True)

    x = torch.linspace(0, 1, 100)
    y = torch.sin(x * (2 * math.pi)) + torch.randn(x.size()) * 0.2

    train_x, fantasy_x = x[:90], x[90:]
    train_y, fantasy_y = y[:90], y[90:]

    class ExactGPModel(gpytorch.models.ExactGP):
        def __init__(self, train_x, train_y, likelihood):
            super().__init__(train_x, train_y, likelihood)
            self.mean_module = gpytorch.means.ConstantMean()
            self.covar_module = gpytorch.kernels.ScaleKernel(gpytorch.kernels.RBFKernel())

        def forward(self, x):
            mean_x = self.mean_module(x)
            covar_x = self.covar_module(x)
            return gpytorch.distributions.MultivariateNormal(mean_x, covar_x)

    likelihood = gpytorch.likelihoods.GaussianLikelihood()
    model = ExactGPModel(train_x, train_y, likelihood)

    print("training model", flush=True)
    model.train()
    likelihood.train()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.1)
    mll = gpytorch.mlls.ExactMarginalLogLikelihood(likelihood, model)

    for _ in range(5):
        optimizer.zero_grad()
        output = model(train_x)
        loss = -mll(output, train_y)
        loss.backward()
        optimizer.step()

    print("creating fantasy model", flush=True)
    model.eval()
    test_x = torch.linspace(0, 1, 51)
    _ = model(test_x)
    fantasized_model = model.get_fantasy_model(fantasy_x, fantasy_y)

    class MeanVarModelWrapper(torch.nn.Module):
        def __init__(self, gp):
            super().__init__()
            self.gp = gp

        def forward(self, x):
            output_dist = self.gp(x)
            return output_dist.mean, output_dist.variance

    print("warming up fantasy model under trace_mode", flush=True)
    with torch.no_grad(), gpytorch.settings.fast_pred_var(), gpytorch.settings.trace_mode():
        fantasized_model.eval()
        _ = fantasized_model(test_x)
        print("tracing fantasy model", flush=True)
        torch.jit.trace(MeanVarModelWrapper(fantasized_model), test_x)
        print("trace completed", flush=True)


if __name__ == "__main__":
    sys.exit(main())
