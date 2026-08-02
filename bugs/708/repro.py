#!/usr/bin/env python3
"""Offline reproduction for DSPy issue #8985."""

import dspy
import dspy.clients.lm as lm_module


class ImageDescription(dspy.Signature):
    image: dspy.Image = dspy.InputField()
    image_description: str = dspy.OutputField()


class ResponsesValidationError(Exception):
    """The deterministic subset of OpenAI Responses validation used by this repro."""


def offline_responses(**request):
    """Capture the converted request without making a provider/network call."""
    content = request["input"][0]["content"]
    types = [block["type"] for block in content]

    # These assertions prove the full DSPy adapter + Responses converter emitted the
    # incompatible Chat Completions blocks for the image request.
    assert "image_url" in types, types
    if "text" in types:
        raise ResponsesValidationError(
            "Invalid value: 'text'. Supported values are: 'input_text', "
            "'input_image', 'output_text', 'refusal', 'input_file', "
            "'computer_screenshot', and 'summary_text'. "
            f"(DSPy content types: {', '.join(types)})"
        )
    raise AssertionError(f"bug absent: Responses content types were {types}")


def main():
    lm_module.litellm.responses = offline_responses
    lm = dspy.LM(
        "openai/gpt-5-mini",
        model_type="responses",
        temperature=1.0,
        max_tokens=16000,
        cache=False,
    )
    messages = dspy.ChatAdapter().format(
        ImageDescription,
        [],
        {"image": dspy.Image("data:image/png;base64,iVBORw0KGgo=")},
    )

    try:
        lm(messages=messages)
    except ResponsesValidationError as error:
        assert "Invalid value: 'text'" in str(error), error
        print(f"OBSERVED BUG: {error}")
        raise RuntimeError("BUG REPRODUCED: OpenAI Responses image payload is malformed") from error

    raise AssertionError("offline Responses validation was not invoked")


if __name__ == "__main__":
    main()
