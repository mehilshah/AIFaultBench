import torch
import torchaudio
import torchaudio.functional as F


def main() -> None:
    print(f"torch={torch.__version__}")
    print(f"torchaudio={torchaudio.__version__}")

    # This mirrors examples/mms/data_prep/align_and_segment.py:
    # it feeds a 2-D emission tensor into forced_align.
    emissions = torch.randn(6, 4, dtype=torch.float32).log_softmax(dim=-1)
    targets = torch.tensor([[1, 2]], dtype=torch.int64)
    input_lengths = torch.tensor([emissions.shape[0]], dtype=torch.int64)
    target_lengths = torch.tensor([targets.shape[1]], dtype=torch.int64)

    print(f"emissions_shape={tuple(emissions.shape)}")
    print(f"targets_shape={tuple(targets.shape)}")
    print("calling torchaudio.functional.forced_align...")

    F.forced_align(
        emissions,
        targets,
        input_lengths=input_lengths,
        target_lengths=target_lengths,
        blank=0,
    )


if __name__ == "__main__":
    main()
