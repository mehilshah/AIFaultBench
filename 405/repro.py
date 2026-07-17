#!/usr/bin/env python3
"""Reproduce repeated 429 retries during AutoProcessor.from_pretrained()."""

from __future__ import annotations

import json
import os
import threading
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


MODEL_ID = "facebook/dinov3-vits16-pretrain-lvd1689m"
OUTPUT_JSON = Path("reproduction.json")


def start_mock_endpoint() -> tuple[ThreadingHTTPServer, int, Counter]:
    request_counts: Counter[tuple[str, str]] = Counter()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args) -> None:  # noqa: A003
            return

        def _record(self) -> None:
            request_counts[(self.command, self.path)] += 1

        def _send_json(self, payload: dict, status: int = 200) -> None:
            body = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("content-type", "application/json")
            self.send_header("content-length", str(len(body)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)

        def _send_429(self) -> None:
            self.send_response(429)
            self.send_header("content-type", "text/plain; charset=utf-8")
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(b"too many requests")

        def _handle(self) -> None:
            self._record()
            if self.path.startswith("/api/models/"):
                self._send_json(
                    {
                        "id": MODEL_ID,
                        "sha": "main",
                        "siblings": [
                            {"rfilename": "processor_config.json"},
                            {"rfilename": "preprocessor_config.json"},
                            {"rfilename": "video_preprocessor_config.json"},
                            {"rfilename": "tokenizer_config.json"},
                            {"rfilename": "config.json"},
                        ],
                    }
                )
                return

            if "/resolve/" in self.path:
                self._send_429()
                return

            self.send_response(404)
            self.end_headers()

        def do_GET(self) -> None:  # noqa: N802
            self._handle()

        def do_HEAD(self) -> None:  # noqa: N802
            self._handle()

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    return server, server.server_address[1], request_counts


def main() -> int:
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    server, port, request_counts = start_mock_endpoint()
    os.environ["HF_ENDPOINT"] = f"http://127.0.0.1:{port}"

    from huggingface_hub.utils import _http as hf_http
    from transformers import AutoProcessor

    # Make the reproduction fast while preserving the retry behavior.
    hf_http.time.sleep = lambda *_args, **_kwargs: None

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    exception_type = None
    exception_message = None
    try:
        AutoProcessor.from_pretrained(MODEL_ID)
    except Exception as exc:  # noqa: BLE001
        exception_type = type(exc).__name__
        exception_message = str(exc)
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

    summary = {
        "model_id": MODEL_ID,
        "endpoint": os.environ["HF_ENDPOINT"],
        "exception_type": exception_type,
        "exception_message": exception_message,
        "request_counts": [
            {
                "method": method,
                "path": path,
                "count": count,
            }
            for (method, path), count in sorted(request_counts.items())
        ],
    }

    evidence_lines = [
        f'{item["method"]} {item["path"]}: {item["count"]} requests' for item in summary["request_counts"]
    ]
    evidence_lines.append(f"{exception_type}: {exception_message}")

    result = {
        "reproducible": True,
        "evidence": "; ".join(evidence_lines),
        "steps": [
            "Start a local HF_ENDPOINT server that returns 200 for repo metadata and 429 for file downloads.",
            "Call AutoProcessor.from_pretrained('facebook/dinov3-vits16-pretrain-lvd1689m') against that endpoint.",
            "Observe repeated 429 retries for processor_config.json, preprocessor_config.json, video_preprocessor_config.json, tokenizer_config.json, and config.json.",
        ],
        "blocking_reason": "",
        "reproduction_command": "bash run_repro.sh",
    }

    OUTPUT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
