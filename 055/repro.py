import json
import os
import platform

import tensorflow as tf
import keras_nlp


def main():
    print(json.dumps(
        {
            "python": platform.python_version(),
            "tensorflow": tf.__version__,
            "keras_nlp": keras_nlp.__version__,
            "gpus": [device.name for device in tf.config.list_physical_devices("GPU")],
            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        },
        indent=2,
        sort_keys=True,
    ))

    sampler = keras_nlp.samplers.GreedySampler()
    prompt = tf.constant([[1, 0, 0, 0]], dtype=tf.int32)
    call_count = {"n": 0}

    def next_fn(prompt, cache, index):
        call_count["n"] += 1
        batch = tf.shape(prompt)[0]
        vocab = 5
        logits = tf.fill((batch, vocab), tf.constant(-1e9, tf.float32))
        logits = tf.tensor_scatter_nd_update(
            logits,
            indices=tf.constant([[0, 3]], dtype=tf.int32),
            updates=tf.constant([0.0], dtype=tf.float32),
        )
        print(
            json.dumps(
                {
                    "step": call_count["n"],
                    "prompt_shape": prompt.shape.as_list(),
                    "index": int(index.numpy()) if hasattr(index, "numpy") else int(index),
                    "cache_len": len(cache),
                    "hidden_states": None,
                },
                sort_keys=True,
            )
        )
        return logits, None, cache

    output = sampler(next_fn, prompt, end_token_id=2, index=1)
    print(json.dumps(
        {
            "output_shape": output.shape.as_list(),
            "output": output.numpy().tolist(),
            "result": "completed_without_segfault",
        },
        indent=2,
        sort_keys=True,
    ))


if __name__ == "__main__":
    main()
