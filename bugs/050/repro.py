#!/usr/bin/env python3
import os

os.environ["KERAS_BACKEND"] = "torch"
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["NVIDIA_VISIBLE_DEVICES"] = "none"

import numpy as np
import torch
import keras
from keras import layers

torch.set_default_device("cpu")


latent_dim = 32
image_shape = (28, 28, 1)
batch_size = 8


def make_generator():
    return keras.Sequential(
        [
            keras.Input(shape=(latent_dim,)),
            layers.Dense(7 * 7 * 128),
            layers.LeakyReLU(negative_slope=0.2),
            layers.Reshape((7, 7, 128)),
            layers.Conv2DTranspose(128, (4, 4), strides=(2, 2), padding="same"),
            layers.LeakyReLU(negative_slope=0.2),
            layers.Conv2DTranspose(128, (4, 4), strides=(2, 2), padding="same"),
            layers.LeakyReLU(negative_slope=0.2),
            layers.Conv2D(1, (7, 7), padding="same", activation="sigmoid"),
        ],
        name="generator",
    )


def make_discriminator():
    return keras.Sequential(
        [
            keras.Input(shape=image_shape),
            layers.Conv2D(128, (3, 3), strides=(2, 2), padding="same"),
            layers.LeakyReLU(negative_slope=0.2),
            layers.Conv2D(128, (3, 3), strides=(2, 2), padding="same"),
            layers.LeakyReLU(negative_slope=0.2),
            layers.Flatten(),
            layers.Dropout(0.2),
            layers.Dense(1),
        ],
        name="discriminator",
    )


class GAN(keras.Model):
    def __init__(self, discriminator, generator, latent_dim):
        super().__init__()
        self.discriminator = discriminator
        self.generator = generator
        self.latent_dim = latent_dim
        self.d_loss_tracker = keras.metrics.Mean(name="d_loss")
        self.g_loss_tracker = keras.metrics.Mean(name="g_loss")
        self.seed_generator = keras.random.SeedGenerator(1337)
        self.built = True

    @property
    def metrics(self):
        return [self.d_loss_tracker, self.g_loss_tracker]

    def compile(self, d_optimizer, g_optimizer, loss_fn):
        super().compile()
        self.d_optimizer = d_optimizer
        self.g_optimizer = g_optimizer
        self.loss_fn = loss_fn

    def train_step(self, real_images):
        device = "cpu"
        print(f"batch type: {type(real_images).__name__}", flush=True)
        if isinstance(real_images, tuple):
            real_images = real_images[0]
        batch_size = real_images.shape[0]
        random_latent_vectors = keras.random.normal(
            shape=(batch_size, self.latent_dim), seed=self.seed_generator
        )
        generated_images = self.generator(random_latent_vectors)
        real_images = torch.tensor(real_images, device=device)
        combined_images = torch.concat([generated_images, real_images], axis=0)
        labels = torch.concat(
            [
                torch.ones((batch_size, 1), device=device),
                torch.zeros((batch_size, 1), device=device),
            ],
            axis=0,
        )
        labels += 0.05 * keras.random.uniform(labels.shape, seed=self.seed_generator)
        self.zero_grad()
        predictions = self.discriminator(combined_images)
        d_loss = self.loss_fn(labels, predictions)
        d_loss.backward()
        grads = [v.value.grad for v in self.discriminator.trainable_weights]
        with torch.no_grad():
            self.d_optimizer.apply(grads, self.discriminator.trainable_weights)

        random_latent_vectors = keras.random.normal(
            shape=(batch_size, self.latent_dim), seed=self.seed_generator
        )
        misleading_labels = torch.zeros((batch_size, 1), device=device)
        self.zero_grad()
        predictions = self.discriminator(self.generator(random_latent_vectors))
        g_loss = self.loss_fn(misleading_labels, predictions)
        g_loss.backward()
        grads = [v.value.grad for v in self.generator.trainable_weights]
        with torch.no_grad():
            self.g_optimizer.apply(grads, self.generator.trainable_weights)

        self.d_loss_tracker.update_state(d_loss)
        self.g_loss_tracker.update_state(g_loss)
        return {
            "d_loss": self.d_loss_tracker.result(),
            "g_loss": self.g_loss_tracker.result(),
        }


def main():
    x = np.random.random((32, *image_shape)).astype("float32")
    dataset = torch.utils.data.TensorDataset(
        torch.from_numpy(x),
        torch.from_numpy(x),
    )
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

    gan = GAN(
        discriminator=make_discriminator(),
        generator=make_generator(),
        latent_dim=latent_dim,
    )
    gan.compile(
        d_optimizer=keras.optimizers.Adam(learning_rate=0.0003),
        g_optimizer=keras.optimizers.Adam(learning_rate=0.0003),
        loss_fn=keras.losses.BinaryCrossentropy(from_logits=True),
    )
    gan.fit(dataloader, epochs=1)


if __name__ == "__main__":
    main()
