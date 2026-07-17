from __future__ import annotations

from pathlib import Path

import torch
from torchrl.record.loggers.csv import CSVLogger


def main() -> None:
    log_dir = Path("results") / "repros"
    logger = CSVLogger(
        exp_name="repro",
        log_dir=str(log_dir),
        video_format="mp4",
    )

    print(f"torch={torch.__version__}")
    try:
        import torchvision

        print(f"torchvision={torchvision.__version__}")
        print(
            "torchvision.io.write_video exists=",
            hasattr(torchvision.io, "write_video"),
        )
    except Exception as exc:
        print(f"torchvision import failed: {exc}")

    video = torch.zeros((1, 2, 3, 4, 4), dtype=torch.uint8)
    print("calling CSVLogger.log_video(...)")
    logger.log_video("repro", video, step=0)
    print("completed")


if __name__ == "__main__":
    main()
