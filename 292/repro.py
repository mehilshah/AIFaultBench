from __future__ import annotations

import sys
import traceback
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
CODEBASE_DIR = ROOT_DIR / "codebase"
if str(CODEBASE_DIR) not in sys.path:
    sys.path.insert(0, str(CODEBASE_DIR))


def main() -> None:
    import numpy as np
    import torch
    import tensordict

    from torchrl.envs import OpenSpielEnv

    print(f"torch={torch.__version__}")
    print(f"tensordict={tensordict.__version__}")
    print(f"numpy={np.__version__}")
    print("constructing OpenSpielEnv('chess', return_state=True, batch_size=(100,))")
    env = OpenSpielEnv("chess", return_state=True, batch_size=(100,))
    print(env)
    print("calling reset()")
    td = env.reset()
    print(td)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
