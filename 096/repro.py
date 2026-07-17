from __future__ import annotations

import sys
from pathlib import Path

import torch


ROOT_DIR = Path(__file__).resolve().parent
CODEBASE_DIR = ROOT_DIR / "codebase"
sys.path.insert(0, str(CODEBASE_DIR))

import denoising_diffusion_pytorch.denoising_diffusion_pytorch as ddp
from denoising_diffusion_pytorch import GaussianDiffusion, Unet


def main() -> int:
    torch.manual_seed(0)

    original_random = ddp.random
    ddp.random = lambda: 0.0

    try:
        model = Unet(dim=16, dim_mults=(1, 2), channels=3, self_condition=True)
        diffusion = GaussianDiffusion(model, image_size=16, timesteps=4)
        img = torch.randn(2, 3, 16, 16, requires_grad=True)

        loss = diffusion(img)
        print(f"torch_version={torch.__version__}")
        print(f"loss={loss.detach().item():.6f}")
        loss.backward()
        print("status=backward_completed")
        print("reproducible=False")
        return 0
    except Exception as exc:  # pragma: no cover - runtime probe only
        print(f"status=exception")
        print(f"exception_type={type(exc).__name__}")
        print(f"exception_message={exc}")
        print("reproducible=True")
        return 1
    finally:
        ddp.random = original_random


if __name__ == "__main__":
    raise SystemExit(main())
