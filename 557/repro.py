from __future__ import annotations

import json

import torch

from diffusers import UNet1DModel


def max_abs_diff(model: UNet1DModel, sample: torch.Tensor, t0: int, t1: int) -> float:
    with torch.no_grad():
        out0 = model(sample, torch.tensor(t0)).sample
        out1 = model(sample, torch.tensor(t1)).sample
    return (out0 - out1).abs().max().item()


def build_default_model() -> UNet1DModel:
    return UNet1DModel(
        sample_size=1024,
        in_channels=1,
        out_channels=1,
        layers_per_block=2,
        block_out_channels=(64, 64, 128, 128, 256),
        down_block_types=("DownBlock1D", "DownBlock1D", "DownBlock1D", "DownBlock1D", "DownBlock1D"),
        up_block_types=("UpBlock1D", "UpBlock1D", "UpBlock1D", "UpBlock1D", "UpBlock1D"),
    )


def build_time_aware_model() -> UNet1DModel:
    return UNet1DModel(
        sample_size=1024,
        in_channels=1,
        out_channels=1,
        layers_per_block=2,
        extra_in_channels=128,
        block_out_channels=(64, 64, 128, 128, 256),
        down_block_types=(
            "DownBlock1DNoSkip",
            "DownBlock1D",
            "DownBlock1D",
            "DownBlock1D",
            "DownBlock1D",
        ),
        up_block_types=("UpBlock1D", "UpBlock1D", "UpBlock1D", "UpBlock1D", "UpBlock1DNoSkip"),
    )


def main() -> None:
    torch.manual_seed(0)
    sample = torch.randn(1, 1, 1024)

    default_model = build_default_model().eval()
    time_aware_model = build_time_aware_model().eval()

    default_diff = max_abs_diff(default_model, sample, 0, 10)
    time_aware_diff = max_abs_diff(time_aware_model, sample, 0, 10)

    result = {
        "default_config_max_abs_diff": default_diff,
        "time_aware_config_max_abs_diff": time_aware_diff,
        "default_config_time_blind": default_diff == 0.0,
        "time_aware_config_time_sensitive": time_aware_diff > 1e-6,
    }

    print(json.dumps(result, indent=2, sort_keys=True))

    assert result["default_config_time_blind"], "Default UNet1DModel config should ignore timestep"
    assert result["time_aware_config_time_sensitive"], "No-skip config should react to timestep"


if __name__ == "__main__":
    main()
