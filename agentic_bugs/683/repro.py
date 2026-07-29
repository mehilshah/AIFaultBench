#!/usr/bin/env python3
"""Reproduce mem0's Qdrant HTTP/API-key TLS selection bug without external services."""

from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

from qdrant_client.http.exceptions import ResponseHandlingException

from mem0.vector_stores.qdrant import Qdrant


class PlainHttpQdrant(BaseHTTPRequestHandler):
    """A deliberately plain-HTTP endpoint; TLS ClientHello bytes trigger the SSL error."""

    def log_message(self, format, *args):
        pass


def main() -> int:
    server = HTTPServer(("127.0.0.1", 0), PlainHttpQdrant)
    Thread(target=server.serve_forever, daemon=True).start()
    try:
        Qdrant(
            collection_name="memories",
            embedding_model_dims=2,
            host="127.0.0.1",
            port=server.server_port,
            api_key="test-key",
        )
    except ResponseHandlingException as error:
        message = str(error)
        if "WRONG_VERSION_NUMBER" in message:
            print("BUG REPRODUCED: host+port+api_key attempted HTTPS against plain HTTP: " + message)
            return 1
        raise
    finally:
        server.shutdown()
        server.server_close()

    print("BUG NOT REPRODUCED: the mem0 Qdrant constructor did not attempt TLS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
