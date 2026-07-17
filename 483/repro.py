from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))


def main() -> None:
    # Import the reported modules in the same order the bug report describes.
    import transformers.models.qwen2_5_vl.modeling_qwen2_5_vl  # noqa: F401
    import transformers.models.qwen3_vl.modeling_qwen3_vl  # noqa: F401
    import transformers.models.glm.modeling_glm  # noqa: F401


if __name__ == "__main__":
    main()
