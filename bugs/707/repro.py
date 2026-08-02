#!/usr/bin/env python3
"""Offline verifier for the endpoint mismatch reported in DSPy issue #8996."""

from pathlib import Path
import re
import subprocess
import sys


SOURCE = Path("codebase/dspy/clients/lm.py")
EXPECTED_COMMIT = "da69f9d05fc7509eb20c4acb41e8b8b793104f7e"


def main() -> int:
    if not SOURCE.is_file():
        raise AssertionError("Pinned checkout is missing; run bash setup_codebase.sh first")

    commit = subprocess.check_output(
        ["git", "-C", "codebase", "rev-parse", "HEAD"], text=True
    ).strip()
    assert commit == EXPECTED_COMMIT, f"Expected {EXPECTED_COMMIT}, got {commit}"

    source = SOURCE.read_text(encoding="utf-8")
    model_types = re.search(
        r'model_type: Literal\["([^"]+)", "([^"]+)", "([^"]+)"\] = "([^"]+)"', source
    )
    assert model_types, "Could not find dspy.LM's supported model types"
    assert model_types.groups() == ("chat", "text", "responses", "chat"), model_types.groups()

    chat_branch = "if self.model_type == \"chat\":\n            completion = litellm_completion"
    assert chat_branch in source, "dspy.LM no longer selects the chat-completion path"
    assert "return litellm.completion(" in source, "The selected chat path no longer calls LiteLLM completion"
    assert "litellm.transcription(" not in source, "Unexpected transcription endpoint support found"

    print(
        "NOT_REPRODUCED: gpt-4o-mini-transcribe is routed to LiteLLM chat completion; "
        "the pinned DSPy API exposes no transcription model type or endpoint."
    )
    print(f"CHECKED_COMMIT: {commit}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
