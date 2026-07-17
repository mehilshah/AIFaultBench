#!/usr/bin/env python3
"""Minimal reproduction for DeepSpeed checkpoint validation on URI-like paths.

This loads only the two helper functions from the checked-out Lightning source
tree, avoiding unrelated import-time failures in the local environment.
"""

from __future__ import annotations

import ast
from pathlib import Path
import sys


CODEBASE_FILE = Path("codebase/src/lightning/fabric/strategies/deepspeed.py")
REMOTE_URI = "s3://my-bucket/checkpoints/epoch=5.ckpt"


def load_helpers() -> dict[str, object]:
    source = CODEBASE_FILE.read_text()
    module = ast.parse(source)
    wanted = {"_is_deepspeed_checkpoint", "_validate_checkpoint_directory"}
    chunks: list[str] = []

    for node in module.body:
        if isinstance(node, ast.FunctionDef) and node.name in wanted:
            chunk = ast.get_source_segment(source, node)
            if chunk is None:
                raise RuntimeError(f"Could not extract {node.name} from {CODEBASE_FILE}")
            chunks.append(chunk)

    namespace: dict[str, object] = {"Path": Path, "_PATH": object}
    exec("from pathlib import Path\n" + "\n\n".join(chunks), namespace)
    return namespace


def main() -> int:
    helpers = load_helpers()
    validate = helpers["_validate_checkpoint_directory"]

    normalized = str(Path(REMOTE_URI))
    print(f"input_uri={REMOTE_URI}")
    print(f"pathlib_normalized={normalized}")

    try:
        validate(REMOTE_URI)
    except FileNotFoundError as exc:
        message = str(exc)
        print(f"raised={type(exc).__name__}")
        print(f"message={message}")

        expected_fragment = "The provided path is not a valid DeepSpeed checkpoint: s3:/my-bucket/checkpoints/epoch=5.ckpt"
        if normalized != "s3:/my-bucket/checkpoints/epoch=5.ckpt":
            print("unexpected_path_normalization")
            return 1
        if expected_fragment not in message:
            print("unexpected_error_message")
            return 1

        print("reproduced=True")
        return 0

    print("reproduced=False")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
