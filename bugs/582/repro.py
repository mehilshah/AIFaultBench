from __future__ import annotations

import os
import sys
import traceback
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR / "codebase" / "src"))

from transformers import BertTokenizer


def main() -> int:
    tokenizer = BertTokenizer(vocab_file=str(ROOT_DIR / "codebase" / "tests" / "fixtures" / "vocab.txt"))
    tokenizer.chat_template = "{{ messages }}"

    print("conversation=[]")
    print("calling apply_chat_template(tokenize=False)")

    try:
        tokenizer.apply_chat_template([], tokenize=False)
    except Exception as exc:  # noqa: BLE001
        print(f"exception_type={type(exc).__name__}")
        print(f"exception_message={exc}")
        traceback.print_exc()
        return 0

    print("unexpected_success=True")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
