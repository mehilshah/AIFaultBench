from __future__ import annotations

import sys
import traceback
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "codebase" / "src" / "diffusers" / "pipelines" / "kandinsky5" / "pipeline_kandinsky_i2i.py"
BUG_SNIPPET = "latents = torch.cat([latents, image_latents, torch.ones_like(latents[..., :1])], -1)"


def main() -> int:
    print(f"python={sys.version.split()[0]}")
    print(f"torch={torch.__version__}")
    print(f"source={SOURCE}")

    if SOURCE.exists():
        for line in SOURCE.read_text().splitlines():
            if BUG_SNIPPET in line:
                print(f"bug_line={line.strip()}")
                break
        else:
            print("bug_line=not found")

    # Simulate the device_map="balanced" split reported in the issue:
    # the noise latents live on one device while the VAE-produced image latents
    # arrive on a different device and the concat fails immediately.
    latents = torch.randn((1, 1, 8, 8, 16), device="cpu")
    image_latents = torch.randn((1, 1, 8, 8, 16), device="meta")

    print(f"noise_device={latents.device}")
    print(f"vae_device={image_latents.device}")

    try:
        torch.cat([latents, image_latents, torch.ones_like(latents[..., :1])], dim=-1)
    except Exception as exc:  # noqa: BLE001 - we want the raw failure for logs
        print(f"expected_failure={type(exc).__name__}: {exc}")
        traceback.print_exc()
        return 1

    print("unexpected_success=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
