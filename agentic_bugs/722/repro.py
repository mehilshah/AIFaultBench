#!/usr/bin/env python3
"""Deterministically expose the released-port race in issue #2704."""

from __future__ import annotations

import ast
import errno
import socket
import sys
from pathlib import Path


FIXTURE_FILE = Path(__file__).parent / "codebase/tests/shared/test_streamable_http.py"


def load_buggy_fixture() -> object:
    """Compile the exact pinned fixture without importing its test dependencies."""
    module = ast.parse(FIXTURE_FILE.read_text(encoding="utf-8"), filename=str(FIXTURE_FILE))
    fixture = next(
        node
        for node in module.body
        if isinstance(node, ast.FunctionDef) and node.name == "basic_server_port"
    )
    fixture.decorator_list = []
    compiled = compile(ast.fix_missing_locations(ast.Module(body=[fixture], type_ignores=[])), str(FIXTURE_FILE), "exec")
    namespace = {"socket": socket}
    exec(compiled, namespace)
    return namespace["basic_server_port"]


def main() -> int:
    basic_server_port = load_buggy_fixture()
    port = basic_server_port()

    # The fixture has returned after its `with socket.socket()` block, so a
    # competing xdist worker can deterministically claim the supposed server port.
    intruder = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    delayed_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        intruder.bind(("127.0.0.1", port))
        intruder.listen()
        try:
            delayed_server.bind(("127.0.0.1", port))
        except OSError as exc:
            if exc.errno != errno.EADDRINUSE:
                raise AssertionError(f"expected EADDRINUSE, got errno={exc.errno}: {exc}") from exc
            print(f"BUG REPRODUCED: basic_server_port released {port}; delayed server bind raised EADDRINUSE")
            return 1
        raise AssertionError("expected the intruder's port reservation to make the delayed server bind fail")
    finally:
        delayed_server.close()
        intruder.close()


if __name__ == "__main__":
    sys.exit(main())
