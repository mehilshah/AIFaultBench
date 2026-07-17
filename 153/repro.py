#!/usr/bin/env python3
from __future__ import annotations

import os
import sys


ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "codebase", "src"))

from transformers import AutoTokenizer, __version__ as transformers_version  # noqa: E402
import tokenizers as tokenizers_lib  # noqa: E402


MODEL_ID = "mlx-community/Llama-3.2-1B-Instruct-4bit"
TOKEN_IDS = [128000, 64, 1174, 65]
EXPECTED = "<|begin_of_text|>a,b"


def main() -> int:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    decoded = tokenizer.decode(TOKEN_IDS)

    print(f"transformers={transformers_version}")
    print(f"tokenizers={tokenizers_lib.__version__}")
    print(f"tokenizer_class={tokenizer.__class__.__name__}")
    print(f"decoded={decoded!r}")
    print(f"expected={EXPECTED!r}")

    if decoded != EXPECTED:
        print("mismatch=observed output differs from the expected v4 behavior")
        return 1

    print("mismatch=none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
