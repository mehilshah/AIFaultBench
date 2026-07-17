import sys

import numpy as np
import scipy
import tensorly as tl


def main():
    print(sys.version)
    print("numpy", np.__version__)
    print("scipy", scipy.__version__)
    print("tensorly", tl.__version__)

    np.set_printoptions(precision=3, floatmode="fixed")
    tl.set_backend("numpy")

    tensor_shape = (32, 32, 32)
    rank_range = list(range(1, 15))
    rng = tl.check_random_state(0)
    tensor = tl.tensor(rng.normal(size=tensor_shape)) + 1j * tl.tensor(
        rng.normal(size=tensor_shape)
    )

    mse = []
    for r in rank_range:
        tensor_approx = tl.tt_to_tensor(tl.decomposition.tensor_train(tensor, rank=r))
        mse.append(tl.mean(tl.abs(tensor_approx - tensor) ** 2))

    mse = np.array(mse)
    print(mse)
    print("first", mse[0], "last", mse[-1], "monotone_nonincreasing", bool(np.all(np.diff(mse) <= 0)))


if __name__ == "__main__":
    main()
