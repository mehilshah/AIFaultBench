import io
import sys
import warnings

import torch

import pyro
import pyro.distributions as dist
from pyro.contrib.easyguide import EasyGuide
from pyro.infer import SVI, Trace_ELBO
from pyro.infer.autoguide.initialization import init_to_median
from pyro.optim import Adam
from pyro.util import ignore_jit_warnings


def model(batch, subsample, full_size):
    with ignore_jit_warnings():
        num_time_steps = len(batch)
    result = [None] * num_time_steps
    drift = pyro.sample("drift", dist.LogNormal(-1, 0.5))
    with pyro.plate("data", full_size, subsample=subsample):
        z = 0.0
        for t in range(num_time_steps):
            z = pyro.sample(f"state_{t}", dist.Normal(z, drift))
            result[t] = pyro.sample(f"obs_{t}", dist.Bernoulli(logits=z), obs=batch[t])
    return torch.stack(result)


class PickleGuide(EasyGuide):
    def __init__(self, model):
        super().__init__(model)
        self.init = init_to_median

    def guide(self, batch, subsample, full_size):
        self.map_estimate("drift")
        with self.plate("data", full_size, subsample=subsample):
            self.group(match="state_[0-9]*").map_estimate()


def check_guide(guide):
    full_size = 50
    batch_size = 20
    num_time_steps = 8
    pyro.set_rng_seed(123456789)
    data = model([None] * num_time_steps, torch.arange(full_size), full_size)
    assert data.shape == (num_time_steps, full_size)

    pyro.get_param_store().clear()
    pyro.set_rng_seed(123456789)
    svi = SVI(model, guide, Adam({"lr": 0.02}), Trace_ELBO())
    for _ in range(2):
        beg = 0
        while beg < full_size:
            end = min(full_size, beg + batch_size)
            subsample = torch.arange(beg, end)
            batch = data[:, beg:end]
            beg = end
            svi.step(batch, subsample, full_size=full_size)


def main():
    guide = PickleGuide(model)
    check_guide(guide)

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        f = io.BytesIO()
        torch.save(guide, f)
        f.seek(0)
        loaded = torch.load(f, weights_only=False)

    print(f"type_matches={type(loaded) == type(guide)}")
    print(f"dir_matches={dir(loaded) == dir(guide)}")

    original_failed = False
    try:
        check_guide(guide)
        print("original_after_save_load=ok")
    except Exception as exc:
        original_failed = True
        print(f"original_after_save_load={type(exc).__name__}: {exc}")

    loaded_ok = False
    try:
        check_guide(loaded)
        loaded_ok = True
        print("loaded_after_save_load=ok")
    except Exception as exc:
        print(f"loaded_after_save_load={type(exc).__name__}: {exc}")

    if original_failed and loaded_ok:
        print("BUG_REPRODUCED")
        return 1

    print("BUG_NOT_REPRODUCED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
