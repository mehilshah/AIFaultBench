#!/usr/bin/env python3
"""Minimal reproduction for the DeepSeek-R1-Distill-Llama-8B tokenizer regression."""

from __future__ import annotations

import json
import sys

from transformers import AutoTokenizer, __version__ as transformers_version


MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"
SAMPLES = [
    "What is 1+1? Answer briefly.",
    "I need to determine the sum of 1 and 1. Adding 1 and 1 gives a total of 2.",
    "First, I recognize that the question is asking for the sum of 1 and 1.",
]


def main() -> int:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    report = {
        "transformers_version": transformers_version,
        "tokenizer_class": type(tokenizer).__name__,
        "legacy": getattr(tokenizer, "legacy", None),
        "bos_token": tokenizer.bos_token,
        "samples": [],
    }

    failed = False
    for text in SAMPLES:
        ids = tokenizer.encode(text)
        decoded = tokenizer.decode(ids)
        expected = f"{tokenizer.bos_token}{text}"
        ok = decoded == expected
        report["samples"].append(
            {
                "input": text,
                "ids": ids,
                "expected": expected,
                "decoded": decoded,
                "match": ok,
            }
        )
        if not ok:
            failed = True

    chat_prompt = tokenizer.apply_chat_template(
        [{"role": "user", "content": "What is 1+1? Answer briefly."}],
        tokenize=False,
        add_generation_prompt=True,
    )
    roundtrip_ids = tokenizer.encode(chat_prompt)
    roundtrip_decoded = tokenizer.decode(roundtrip_ids)
    report["chat_prompt"] = {
        "prompt": chat_prompt,
        "decoded": roundtrip_decoded,
        "match": roundtrip_decoded == chat_prompt,
    }
    if roundtrip_decoded != chat_prompt:
        failed = True

    print(json.dumps(report, indent=2, ensure_ascii=False))

    if failed:
        print("REGRESSION: tokenizer decode does not preserve spaces.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
