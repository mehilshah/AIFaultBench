from __future__ import annotations

import sys


def main() -> int:
    import pytorch_lightning as pl
    import lightning.fabric as fabric

    print(f"pytorch_lightning_import=ok version={pl.__version__}")
    print(f"lightning_fabric_import=ok module={fabric.__file__}")
    print(f"lightning_fabric_has_strategies={hasattr(fabric, 'strategies')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
