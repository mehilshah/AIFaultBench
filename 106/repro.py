import os

import torch

from timm.layers import Mlp


def main() -> None:
    torch.manual_seed(0)

    device_name = os.environ.get("TORCH_DEVICE")
    if device_name is None:
        device_name = "cuda" if torch.cuda.is_available() else "cpu"
    device = torch.device(device_name)

    print(f"device={device}")
    print(f"torch={torch.__version__}")

    x = (torch.rand(1, 499, 1280, device=device) * 1000).repeat(2, 1, 1)
    print(f"inputs_equal={x[0].equal(x[1])}")

    mlp = Mlp(
        in_features=1280,
        hidden_features=5120,
        act_layer=torch.nn.GELU,
        drop=0.0,
    ).to(device)
    mlp.eval()

    with torch.no_grad():
        result_single = mlp(x[:1])
        result_double = mlp(x[:2])

    print(f"double_rows_equal={result_double[0].equal(result_double[1])}")
    max_abs_diff = (result_single[0] - result_double[0]).abs().max().item()
    print(f"max_abs_diff_single_vs_double0={max_abs_diff}")

    assert x[0].equal(x[1]), "inputs are different than one another"
    assert result_double[0].equal(
        result_double[1]
    ), "outputs are different than one another for two identical samples in the same batch"
    assert result_single[0].equal(
        result_double[0]
    ), "outputs are different than one another for two identical samples in batches of different sizes"


if __name__ == "__main__":
    main()
