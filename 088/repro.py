from __future__ import annotations

import sys
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
sys.path.insert(0, str(CODEBASE))

from x_transformers.autoregressive_wrapper import align_right  # noqa: E402


def main() -> None:
    prompts = torch.tensor(
        [
            [11, 12, 13],
            [21, 22, 23],
        ],
        dtype=torch.long,
    )
    prompt_lens = torch.tensor([2, 1], dtype=torch.long)
    pad_id = 9

    aligned = align_right(prompts, prompt_lens, pad_id=pad_id)
    expected = torch.tensor(
        [
            [9, 11, 12],
            [9, 9, 21],
        ],
        dtype=torch.long,
    )

    print("prompts:", prompts.tolist())
    print("prompt_lens:", prompt_lens.tolist())
    print("pad_id:", pad_id)
    print("aligned:", aligned.tolist())
    print("expected:", expected.tolist())

    if not torch.equal(aligned, expected):
        raise AssertionError(
            "align_right ignored pad_id: left padding should use 9, "
            f"but got {aligned.tolist()}"
        )


if __name__ == "__main__":
    main()
