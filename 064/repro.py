#!/usr/bin/env python3
"""Minimal repro for the NER Transformer TFLite shape mismatch."""

import os
import tempfile

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


class TransformerBlock(layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.1):
        super().__init__()
        self.att = keras.layers.MultiHeadAttention(
            num_heads=num_heads, key_dim=embed_dim
        )
        self.ffn = keras.Sequential(
            [
                keras.layers.Dense(ff_dim, activation="relu"),
                keras.layers.Dense(embed_dim),
            ]
        )
        self.layernorm1 = keras.layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = keras.layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = keras.layers.Dropout(rate)
        self.dropout2 = keras.layers.Dropout(rate)

    def call(self, inputs, training=False):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)


class TokenAndPositionEmbedding(layers.Layer):
    def __init__(self, maxlen, vocab_size, embed_dim):
        super().__init__()
        self.token_emb = keras.layers.Embedding(
            input_dim=vocab_size, output_dim=embed_dim
        )
        self.pos_emb = keras.layers.Embedding(input_dim=maxlen, output_dim=embed_dim)

    def call(self, inputs):
        maxlen = tf.shape(inputs)[-1]
        positions = tf.range(start=0, limit=maxlen, delta=1)
        position_embeddings = self.pos_emb(positions)
        token_embeddings = self.token_emb(inputs)
        return token_embeddings + position_embeddings


class NERModel(keras.Model):
    def __init__(
        self, num_tags, vocab_size, maxlen=128, embed_dim=32, num_heads=2, ff_dim=32
    ):
        super().__init__()
        self.embedding_layer = TokenAndPositionEmbedding(maxlen, vocab_size, embed_dim)
        self.transformer_block = TransformerBlock(embed_dim, num_heads, ff_dim)
        self.dropout1 = layers.Dropout(0.1)
        self.ff = layers.Dense(ff_dim, activation="relu")
        self.dropout2 = layers.Dropout(0.1)
        self.ff_final = layers.Dense(num_tags, activation="softmax")

    def call(self, inputs, training=False):
        x = self.embedding_layer(inputs)
        x = self.transformer_block(x)
        x = self.dropout1(x, training=training)
        x = self.ff(x)
        x = self.dropout2(x, training=training)
        x = self.ff_final(x)
        return x


def main():
    tf.random.set_seed(0)
    np.random.seed(0)

    build_input = tf.constant([[1]], dtype=tf.int64)
    sample_input = tf.constant([[1, 2, 3, 4, 5, 6, 7, 8, 9]], dtype=tf.int64)

    model = NERModel(
        num_tags=5, vocab_size=50, maxlen=128, embed_dim=8, num_heads=2, ff_dim=16
    )
    _ = model(build_input)
    print("Keras output shape:", model(sample_input).shape)

    custom_objects = {
        "NERModel": NERModel,
        "TransformerBlock": TransformerBlock,
        "TokenAndPositionEmbedding": TokenAndPositionEmbedding,
    }

    with tempfile.TemporaryDirectory(prefix="ner_tflite_") as saved_model_dir:
        model.save(saved_model_dir)
        print("SavedModel dir:", saved_model_dir)

        loaded = keras.models.load_model(
            saved_model_dir, custom_objects=custom_objects, compile=False
        )
        print("Reloaded model type:", type(loaded).__name__)

        converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
        tflite_model = converter.convert()
        tflite_path = os.path.join(saved_model_dir, "model.tflite")
        with open(tflite_path, "wb") as f:
            f.write(tflite_model)

        interpreter = tf.lite.Interpreter(model_path=tflite_path)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()[0]
        print("TFLite input details:", input_details)

        input_index = input_details["index"]
        try:
            interpreter.set_tensor(input_index, np.expand_dims(sample_input.numpy()[0], 0))
            interpreter.invoke()
            print("TFLite invoke succeeded unexpectedly.")
        except Exception as exc:
            print("EXPECTED_FAILURE:", type(exc).__name__, exc)


if __name__ == "__main__":
    main()
