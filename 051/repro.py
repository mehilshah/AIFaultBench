#!/usr/bin/env python3
"""Minimal reproduction for the GreedySampler keyword mismatch."""

import keras
import keras_nlp
from keras import ops


def decode_sequences():
    """Recreate the sampler call site from the issue report."""

    batch_size = 1
    prompt = ops.array([[2, 0, 0]], dtype="int32")

    def next(prompt, cache, index):
        del prompt, cache, index
        logits = ops.zeros((batch_size, 4), dtype="float32")
        hidden_states = None
        return logits, hidden_states, cache

    sampler = keras_nlp.samplers.GreedySampler()
    return sampler(
        next,
        prompt,
        end_token_id=1,
        index=1,
    )


def main():
    print(f"keras={keras.__version__}")
    print(f"keras_nlp={keras_nlp.__version__}")
    print("calling GreedySampler with end_token_id...")
    decode_sequences()


if __name__ == "__main__":
    main()
