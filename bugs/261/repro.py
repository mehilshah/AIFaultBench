#!/usr/bin/env python3
"""Minimal reproduction for stanza Portuguese URL sentence splitting."""

import json
import os
import sys

import stanza


ROOT = os.path.abspath(os.path.dirname(__file__))
MODEL_DIR = os.path.join(ROOT, "stanza_resources")

FAIL_TEXT = (
    "Olá, não deixe de visitar nossos sites em "
    "exemplo1.com, exemplo2.com e exemplo3.com.br"
)
FAIL_EXPECTED = [
    "Olá, não deixe de visitar nossos sites em exemplo1.com, "
    "exemplo2.com e exemplo3.com.br",
]

CONTROL_TEXT = (
    "Olá, não deixe de visitar nossos sites em "
    "www.exemplo1.com, www.exemplo2.com e www.exemplo3.com.br"
)
CONTROL_EXPECTED = [
    "Olá, não deixe de visitar nossos sites em "
    "www.exemplo1.com, www.exemplo2.com e www.exemplo3.com.br",
]


def run_pipeline(text):
    nlp = stanza.Pipeline(
        lang="pt",
        processors="tokenize",
        dir=MODEL_DIR,
        download_method=None,
        verbose=False,
    )
    return [sentence.text for sentence in nlp(text).sentences]


def main():
    stanza.download("pt", processors="tokenize", model_dir=MODEL_DIR, verbose=False)

    fail_actual = run_pipeline(FAIL_TEXT)
    control_actual = run_pipeline(CONTROL_TEXT)

    print(f"stanza_version={stanza.__version__}")
    print("fail_text=", FAIL_TEXT)
    print("fail_actual=", json.dumps(fail_actual, ensure_ascii=False))
    print("fail_expected=", json.dumps(FAIL_EXPECTED, ensure_ascii=False))
    print("control_text=", CONTROL_TEXT)
    print("control_actual=", json.dumps(control_actual, ensure_ascii=False))
    print("control_expected=", json.dumps(CONTROL_EXPECTED, ensure_ascii=False))

    if fail_actual != FAIL_EXPECTED:
        print("BUG_REPRODUCED: Portuguese URLs are split into separate sentences.")
        return 1

    print("BUG_NOT_REPRODUCED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
