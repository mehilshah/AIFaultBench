#!/usr/bin/env python3
"""Reproduce SWE-agent #1012 without a model or external service."""

import importlib.util
import logging
import sys
import tempfile
from pathlib import Path


def load_buggy_log_module():
    source = Path(__file__).parent / "codebase" / "sweagent" / "utils" / "log.py"
    spec = importlib.util.spec_from_file_location("sweagent_buggy_log", source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    module = load_buggy_log_module()
    original_file_handler = logging.FileHandler

    class CP1252DefaultFileHandler(original_file_handler):
        """Model Windows' cp1252 default only when SWE-agent omits encoding."""

        def __init__(self, filename, mode="a", encoding=None, delay=False, errors=None):
            super().__init__(filename, mode, encoding or "cp1252", delay, errors)

    with tempfile.TemporaryDirectory() as directory:
        log_path = Path(directory) / "agent.log"
        logging.FileHandler = CP1252DefaultFileHandler
        try:
            module.add_file_handler(log_path, id_="bug-717")
        finally:
            logging.FileHandler = original_file_handler

        logger = module.get_logger("bug-717")
        file_handler = next(
            handler for handler in logger.handlers if getattr(handler, "baseFilename", None) == str(log_path)
        )
        assert file_handler.stream.encoding.lower() == "cp1252"
        logger.info("🤖 MODEL INPUT")
        file_handler.flush()

        assert log_path.read_bytes() == b"", "the cp1252 handler unexpectedly wrote the emoji"
        print("OBSERVED BUG: UnicodeEncodeError for U+1F916 with cp1252 FileHandler", flush=True)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
