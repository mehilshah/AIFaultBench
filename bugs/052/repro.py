import os

os.environ["KERAS_BACKEND"] = "tensorflow"
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import tensorflow as tf
import keras
from keras import layers


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


class CustomNonPaddingTokenLoss(keras.losses.Loss):
    def __init__(self, name="custom_ner_loss"):
        super().__init__(name=name)

    def call(self, y_true, y_pred):
        loss_fn = keras.losses.SparseCategoricalCrossentropy(
            from_logits=False, reduction=None
        )
        loss = loss_fn(y_true, y_pred)
        mask = tf.cast((y_true > 0), dtype=tf.float32)
        loss = loss * mask
        return tf.reduce_sum(loss) / tf.reduce_sum(mask)


def make_dataset():
    xs = [
        tf.constant([1, 2, 3], dtype=tf.int64),
        tf.constant([1, 3, 4, 2], dtype=tf.int64),
        tf.constant([2, 4, 3, 1, 5], dtype=tf.int64),
    ]
    ys = [
        tf.constant([1, 2, 0], dtype=tf.int64),
        tf.constant([1, 0, 2, 3], dtype=tf.int64),
        tf.constant([1, 2, 3, 4, 0], dtype=tf.int64),
    ]
    ds = tf.data.Dataset.from_generator(
        lambda: zip(xs, ys),
        output_signature=(
            tf.TensorSpec(shape=(None,), dtype=tf.int64),
            tf.TensorSpec(shape=(None,), dtype=tf.int64),
        ),
    )
    return ds.padded_batch(2)


def main():
    print("TensorFlow:", tf.__version__)
    print("Keras:", keras.__version__)
    model = NERModel(num_tags=5, vocab_size=20, embed_dim=32, num_heads=4, ff_dim=64)
    model.compile(optimizer="adam", loss=CustomNonPaddingTokenLoss())

    ds = make_dataset()
    history = model.fit(ds, epochs=1, verbose=1)
    print("fit_history_keys:", sorted(history.history.keys()))

    sample_input = tf.constant([[1, 2, 3, 4]], dtype=tf.int64)
    output = model.predict(sample_input, verbose=0)
    print("predict_shape:", tuple(output.shape))
    print("prediction_argmax:", np.argmax(output, axis=-1).tolist())
    print("RESULT: success")


if __name__ == "__main__":
    main()
