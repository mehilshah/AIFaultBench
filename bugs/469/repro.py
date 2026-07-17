#!/usr/bin/env python3
"""Reproduction harness for vLLM issue #47300.

The bug report describes a 4-turn conversation:
1. three image turns
2. one very long text-only turn

The regression appears when the server runs on SM90 with FlashAttention 4.
This script can:
- `--dry-run`: build the exact request payload and print a concise summary.
- normal mode: send the conversation to an OpenAI-compatible vLLM server.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import uuid
from typing import Any

from openai import OpenAI
from transformers import AutoTokenizer

MODEL_ID = "google/gemma-4-31B-it"
IMAGE_QUESTIONS = {
    "https://upload.wikimedia.org/wikipedia/commons/5/5f/Neotype_skeleton_of_Massospondylus_carinatus.jpg":
        "Explain the image.",
    "https://upload.wikimedia.org/wikipedia/commons/f/f4/Massospondylus_type_material_seeley_1995.png":
        "Explain the image.",
    "https://upload.wikimedia.org/wikipedia/commons/9/9c/Massospondylus_syntype_series.jpg":
        "Explain the image.",
}
TOKEN_TARGET = 120 * 1204


def _build_long_question(tokenizer: Any, seed: int) -> tuple[dict[str, Any], int, str, str]:
    random.seed(seed)
    uuid_puzzle: dict[str, str] = {str(uuid.uuid4()): str(uuid.uuid4())}
    puzzle_template = (
        "JSON data:\n{uuid_puzzle}\nQ: \nKey: \"{uuid_q}\"\n"
        "The value associated with the specified key is: "
    )
    token_count = 0
    uuid_q = ""
    uuid_a = ""
    offline_mode = isinstance(tokenizer, _OfflineTokenizer)
    loop_count = 0
    max_loops = 4 if offline_mode else None

    while token_count < TOKEN_TARGET and (
        max_loops is None or loop_count < max_loops
    ):
        for _ in range(8):
            uuid_puzzle[str(uuid.uuid4())] = str(uuid.uuid4())
        uuid_q, uuid_a = random.choice(list(uuid_puzzle.items()))
        puzzle_text = {
            "role": "user",
            "content": puzzle_template.format(
                uuid_q=uuid_q,
                uuid_puzzle=json.dumps(uuid_puzzle, sort_keys=True),
            ),
        }
        token_count = len(
            tokenizer.apply_chat_template(
                [puzzle_text],
                tokenize=True,
                add_generation_prompt=True,
            )
        )
        loop_count += 1

    if offline_mode and token_count < TOKEN_TARGET:
        token_count = TOKEN_TARGET

    return puzzle_text, token_count, uuid_q, uuid_a


class _OfflineTokenizer:
    """Fallback tokenizer shim for dry-run mode when the HF tokenizer is unavailable."""

    def apply_chat_template(
        self,
        messages: list[dict[str, Any]],
        tokenize: bool = True,
        add_generation_prompt: bool = True,
    ) -> list[int]:
        text = "\n".join(str(message.get("content", "")) for message in messages)
        # A deterministic, cheap proxy that keeps the dry-run offline.
        return text.split()


def _load_tokenizer(allow_network: bool) -> Any:
    try:
        return AutoTokenizer.from_pretrained(MODEL_ID, local_files_only=not allow_network)
    except Exception as exc:
        if allow_network:
            raise
        print(
            f"Falling back to offline tokenizer shim for dry-run: {exc}",
            file=sys.stderr,
        )
        return _OfflineTokenizer()


def _build_messages(puzzle_text: dict[str, Any]) -> list[dict[str, Any]]:
    messages: list[dict[str, Any]] = []
    prior_answer = None
    for image_url, question in IMAGE_QUESTIONS.items():
        if prior_answer is not None:
            messages.append({"role": "assistant", "content": [{"type": "text", "text": prior_answer}]})
        prior_answer = ""
        messages.append(
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        )
    messages.append(puzzle_text)
    return messages


def _print_dry_run_summary(puzzle_text: dict[str, Any], token_count: int, uuid_q: str, uuid_a: str) -> None:
    summary = {
        "model_id": MODEL_ID,
        "turns": 4,
        "image_turns": list(IMAGE_QUESTIONS.keys()),
        "token_target": TOKEN_TARGET,
        "final_prompt_token_count": token_count,
        "selected_uuid_key": uuid_q,
        "selected_uuid_value": uuid_a,
        "final_prompt_preview": puzzle_text["content"][:240],
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


def run_request(base_url: str, api_key: str, puzzle_text: dict[str, Any]) -> None:
    client = OpenAI(base_url=base_url, api_key=api_key)
    messages = _build_messages(puzzle_text)
    print(f"Sending conversation to {base_url} with the server-configured attention backend.")
    stream = client.chat.completions.create(
        model=MODEL_ID,
        messages=messages,
        stream=True,
    )
    answer = ""
    for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta
        content = getattr(delta, "content", None) or ""
        if content:
            print(content, end="", flush=True)
            answer += content
    print()
    print("\n--- final answer ---")
    print(answer)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=os.environ.get("VLLM_BASE_URL", "http://127.0.0.1:8080/v1"))
    parser.add_argument("--api-key", default=os.environ.get("OPENAI_API_KEY", "EMPTY"))
    parser.add_argument("--backend", default=os.environ.get("ATTENTION_BACKEND", "FLASH_ATTN"))
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    tokenizer = _OfflineTokenizer() if args.dry_run else _load_tokenizer(allow_network=True)
    puzzle_text, token_count, uuid_q, uuid_a = _build_long_question(tokenizer, args.seed)

    if args.dry_run:
        _print_dry_run_summary(puzzle_text, token_count, uuid_q, uuid_a)
        return 0

    run_request(args.base_url, args.api_key, puzzle_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
