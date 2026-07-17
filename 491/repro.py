from __future__ import annotations

import torch
from torchrl.data import Bounded, Composite


def main() -> None:
    shape = (2,)
    ts = Composite(
        obs=Bounded(
            torch.zeros(*shape, 3),
            torch.ones(*shape, 3),
        ),
        shape=shape,
    )
    r = ts.rand()
    raw_vals = {"obs": r["obs"].cpu().numpy()}
    encoded_vals = ts.encode(raw_vals)

    print(ts.shape)
    print(r.batch_size)
    print(encoded_vals.batch_size)
    print("matches_expected:", encoded_vals.batch_size == ts.shape)


if __name__ == "__main__":
    main()
