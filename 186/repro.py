from __future__ import annotations

import base64
import os
import socket
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from types import SimpleNamespace

import uvicorn
from starlette.websockets import WebSocket

from marimo._server.api.middleware import ProxyMiddleware
from marimo._server.main import create_starlette_app
from marimo._session.model import SessionMode


BASE_URL = "/my/custom/path"
LSP_PATH = "/lsp/pylsp"
PREFIXED_LSP_PATH = f"{BASE_URL}{LSP_PATH}"


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@dataclass
class DummyLspServer:
    id: str
    port: int


async def _mock_proxy_websocket(self, scope, receive, send, ws_url):
    websocket = WebSocket(scope, receive=receive, send=send)
    await websocket.accept()
    await websocket.close(code=1000, reason=f"mocked upstream for {ws_url}")


def _run_curl(port: int, path: str) -> tuple[int, str]:
    key = base64.b64encode(os.urandom(16)).decode("utf-8")
    cmd = [
        "curl",
        "--http1.1",
        "-i",
        "-N",
        "-sS",
        "-H",
        "Connection: Upgrade",
        "-H",
        "Upgrade: websocket",
        "-H",
        f"Sec-WebSocket-Key: {key}",
        "-H",
        "Sec-WebSocket-Version: 13",
        "-H",
        "Origin: http://localhost:8000",
        f"http://127.0.0.1:{port}{path}",
    ]
    completed = subprocess.run(
        cmd, capture_output=True, text=False, check=False
    )
    stdout = completed.stdout.decode("utf-8", errors="replace")
    stderr = completed.stderr.decode("utf-8", errors="replace")
    return completed.returncode, stdout + stderr


def _extract_status(output: str) -> str:
    for line in output.splitlines():
        if line.startswith("HTTP/"):
            return line.strip()
    return "<no http status found>"


def main() -> int:
    ProxyMiddleware._proxy_websocket = _mock_proxy_websocket  # type: ignore[method-assign]

    app = create_starlette_app(
        base_url=BASE_URL,
        enable_auth=False,
        skew_protection=False,
        lsp_servers=[DummyLspServer(id="pylsp", port=_find_free_port())],
    )
    app.state.session_manager = SimpleNamespace(mode=SessionMode.EDIT)

    port = _find_free_port()
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=port,
        log_level="error",
        access_log=False,
    )
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    deadline = time.time() + 10
    while not server.started and time.time() < deadline:
        time.sleep(0.05)

    if not server.started:
        print("Server failed to start", file=sys.stderr)
        return 2

    try:
        _, prefixed_out = _run_curl(port, PREFIXED_LSP_PATH)
        _, root_out = _run_curl(port, LSP_PATH)

        prefixed_status = _extract_status(prefixed_out)
        root_status = _extract_status(root_out)

        print("Prefixed path:", PREFIXED_LSP_PATH, flush=True)
        print(prefixed_status, flush=True)
        print(prefixed_out, flush=True)
        print("Root path:", LSP_PATH, flush=True)
        print(root_status, flush=True)
        print(root_out, flush=True)

        if "404 Not Found" not in prefixed_status and "403 Forbidden" not in prefixed_status:
            print(
                "Expected the base-url-prefixed LSP websocket to fail with 404 or 403.",
                file=sys.stderr,
            )
            return 1

        if "101 Switching Protocols" not in root_status:
            print(
                "Expected the root LSP websocket to upgrade successfully.",
                file=sys.stderr,
            )
            return 1

        print("Reproduced base-url mismatch for pylsp websocket routing.", flush=True)
        return 0
    finally:
        server.should_exit = True
        thread.join(timeout=10)


if __name__ == "__main__":
    raise SystemExit(main())
