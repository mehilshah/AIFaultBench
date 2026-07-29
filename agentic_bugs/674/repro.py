#!/usr/bin/env python3
"""Offline reproduction for DSPy's non-transactional state loading bug."""

import json
import tempfile
from pathlib import Path

import dspy
from dspy.primitives.example import Example


class Sig(dspy.Signature):
    question: str = dspy.InputField()
    answer: str = dspy.OutputField()


class Prog(dspy.Module):
    def __init__(self):
        super().__init__()
        self.a = dspy.ChainOfThought(Sig)
        self.b = dspy.ChainOfThought(Sig)


def main() -> None:
    source = Prog()
    sentinel = Example(question="q1", answer="a1").with_inputs("question")
    source.a.predict.demos = [sentinel]
    source.b.predict.demos = [sentinel]

    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "state.json"
        source.save(str(path), save_program=False)
        state = json.loads(path.read_text())
        path.write_text(json.dumps({key: value for key, value in state.items() if "b." not in key}))

        template = Prog()
        assert template.a.predict.demos == []
        try:
            template.load(str(path))
        except KeyError as exc:
            assert exc.args == ("b.predict",), exc
        else:
            raise AssertionError("expected the corrupted state to raise KeyError('b.predict')")

        actual = template.a.predict.demos
        expected = [{"question": "q1", "answer": "a1"}]
        assert actual == expected, (actual, expected)
        print("OBSERVED BUG: KeyError('b.predict') left a.predict.demos partially loaded")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
