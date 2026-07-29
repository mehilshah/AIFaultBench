#!/usr/bin/env python3
"""Offline reproducer for DSPy's GEPA reasoning-output regression."""

from types import SimpleNamespace

import dspy
from dspy.teleprompt.gepa.gepa_utils import DspyAdapter


class ReasoningLM(dspy.BaseLM):
    """A no-network LM response shaped like an OpenAI reasoning completion."""

    def __init__(self):
        super().__init__(model="stub/reasoning-model")

    def forward(self, prompt=None, messages=None, **kwargs):
        message = SimpleNamespace(content="improved instruction", reasoning_content="stub reasoning")
        return SimpleNamespace(
            choices=[SimpleNamespace(message=message)],
            usage={},
            model=self.model,
        )


def main():
    lm = ReasoningLM()
    output = lm("verify the BaseLM contract")[0]
    assert output == {"text": "improved instruction", "reasoning_content": "stub reasoning"}, output

    adapter = DspyAdapter(
        student_module=None,
        metric_fn=lambda *_args, **_kwargs: 0.0,
        feedback_map={},
        reflection_lm=lm,
    )
    try:
        adapter.propose_new_texts(
            candidate={"predictor": "original instruction"},
            reflective_dataset={"predictor": []},
            components_to_update=["predictor"],
        )
    except AttributeError as error:
        expected = "'dict' object has no attribute 'strip'"
        assert str(error) == expected, repr(error)
        print(f"OBSERVED BUG: BaseLM returned dict; GEPA raised AttributeError: {error}")
        raise
    raise AssertionError("Expected GEPA to call .strip() on the reasoning-output dict")


if __name__ == "__main__":
    main()
