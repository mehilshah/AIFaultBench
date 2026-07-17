from __future__ import annotations

import traceback
from pathlib import Path


def main() -> None:
    source = Path("codebase/tutorials/sphinx-tutorials/coding_ppo.py")
    print(f"source_file: {source}")
    print("repro: executing the visible tutorial snippet without the hidden multiprocessing import")
    print("source_evidence: hidden import block is wrapped in sphinx_gallery_start_ignore at lines 108-119")
    print("source_evidence: visible failure point is `is_fork = multiprocessing.get_start_method() == \"fork\"` at line 160")

    snippet = """
import warnings

warnings.filterwarnings("ignore")

is_fork = multiprocessing.get_start_method() == "fork"
print(is_fork)
"""
    try:
        exec(snippet, {})
    except Exception:
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
