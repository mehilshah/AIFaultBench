#!/usr/bin/env python3
"""Reproduce RemoteGraph's rejected context + configurable request locally."""

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import httpx
from langgraph.pregel.remote import RemoteGraph


class RejectContextAndConfigurable(BaseHTTPRequestHandler):
    received: dict[str, object] | None = None

    def log_message(self, format: str, *args: object) -> None:
        pass

    def do_POST(self) -> None:
        size = int(self.headers["Content-Length"])
        type(self).received = {"path": self.path, "body": json.loads(self.rfile.read(size))}
        body = {
            "detail": "Cannot specify both configurable and context. Prefer setting context alone."
        }
        encoded = json.dumps(body).encode()
        self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


server = ThreadingHTTPServer(("127.0.0.1", 0), RejectContextAndConfigurable)
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()

try:
    url = f"http://127.0.0.1:{server.server_port}"
    graph = RemoteGraph("agent", url=url)
    try:
        list(
            graph.stream(
                {"messages": [{"role": "user", "content": "hello"}]},
                config={"configurable": {"thread_id": "bug-thread"}},
                context={"user_id": "123"},
                stream_mode="values",
            )
        )
    except httpx.HTTPStatusError as error:
        request = RejectContextAndConfigurable.received
        assert request == {
            "path": "/threads/bug-thread/runs/stream",
            "body": {
                "input": {"messages": [{"role": "user", "content": "hello"}]},
                "config": {"configurable": {"thread_id": "bug-thread"}},
                "context": {"user_id": "123"},
                "stream_mode": ["values", "updates"],
                "stream_subgraphs": False,
                "stream_resumable": False,
                "assistant_id": "agent",
                "if_not_exists": "create",
            },
        }, request
        assert error.response.status_code == 400
        assert error.response.json()["detail"] == (
            "Cannot specify both configurable and context. Prefer setting context alone."
        )
        print("BUG REPRODUCED: context plus configurable is rejected with HTTP 400.")
        raise AssertionError("buggy RemoteGraph request was rejected") from None
    raise AssertionError("expected the combined context/config request to be rejected")
finally:
    server.shutdown()
    server.server_close()
