#!/usr/bin/env python3
"""Check the withdrawn GEPA minibatch claim without calling an LLM."""

from types import SimpleNamespace

import dspy
import gepa
from gepa.api import optimize
from gepa.core.adapter import EvaluationBatch


class SilentLogger:
    def log(self, _message):
        pass


class RecordingAdapter:
    def __init__(self):
        self.reflection_sizes = []

    def evaluate(self, batch, _candidate, capture_traces=False):
        return EvaluationBatch(
            outputs=list(batch),
            scores=[0.0] * len(batch),
            trajectories=list(batch) if capture_traces else None,
        )

    def make_reflective_dataset(self, _candidate, eval_batch, _components):
        self.reflection_sizes.append(len(eval_batch.trajectories))
        return {"predictor": []}

    def propose_new_texts(self, candidate, _dataset, _components):
        return {"predictor": candidate["predictor"] + " updated"}


def verify_dspy_forwards_the_parameter():
    captured = {}
    original_optimize = gepa.optimize

    def fake_optimize(**kwargs):
        captured.update(kwargs)
        return SimpleNamespace(best_candidate=kwargs["seed_candidate"])

    gepa.optimize = fake_optimize
    try:
        optimizer = dspy.GEPA(
            metric=lambda gold, pred, trace, pred_name, pred_trace: 0.0,
            max_metric_calls=10,
            reflection_minibatch_size=3,
            instruction_proposer=lambda **_kwargs: {},
        )
        optimizer.compile(
            dspy.Predict("x -> y"),
            trainset=[dspy.Example(x="input").with_inputs("x")],
        )
    finally:
        gepa.optimize = original_optimize

    assert captured["reflection_minibatch_size"] == 3, captured


def main():
    verify_dspy_forwards_the_parameter()

    adapter = RecordingAdapter()
    optimize(
        seed_candidate={"predictor": "base"},
        trainset=list(range(10)),
        valset=["validation"],
        adapter=adapter,
        reflection_minibatch_size=3,
        max_metric_calls=10,
        use_merge=False,
        logger=SilentLogger(),
        display_progress_bar=False,
        seed=0,
    )

    assert adapter.reflection_sizes, "GEPA made no reflective batches"
    assert set(adapter.reflection_sizes) == {3}, adapter.reflection_sizes
    print(f"NOT REPRODUCED: DSPy forwarded 3; GEPA reflection batches were {adapter.reflection_sizes}.")


if __name__ == "__main__":
    main()
