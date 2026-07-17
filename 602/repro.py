from __future__ import annotations

import functools
import os
import sys
import traceback
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"


def main() -> int:
    # Keep downloads local to this repro folder.
    os.environ.setdefault("TORCH_HOME", str(ROOT / ".torch_home"))
    sys.path.insert(0, str(CODEBASE))

    import torch
    import torch.hub
    from torchrl.envs.transforms import VIPTransform

    # Preserve the load behavior but silence the progress bar so the log stays small.
    original_download = torch.hub.download_url_to_file

    @functools.wraps(original_download)
    def quiet_download_url_to_file(url, dst, hash_prefix=None, progress=True):
        return original_download(url, dst, hash_prefix=hash_prefix, progress=False)

    torch.hub.download_url_to_file = quiet_download_url_to_file

    print(f"torch={torch.__version__}")
    print("constructing VIPTransform(model_name='resnet50', download=True)")
    transform = VIPTransform(model_name="resnet50", download=True)
    print(f"constructed={type(transform).__name__}")
    print("status=success")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        traceback.print_exc()
        raise SystemExit(1)
