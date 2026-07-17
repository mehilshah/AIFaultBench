import os

os.environ.setdefault("KERAS_BACKEND", "tensorflow")

import numpy as np

import keras
from keras import layers, ops


def main():
    print(f"keras={keras.__version__}")
    print(f"backend={keras.backend.backend()}")

    image_size = 72
    patch_size = 6

    # Match the issue report: convert an integer image to a tensor, resize it,
    # then feed it directly into the example's Patches layer.
    rng = np.random.default_rng(1337)
    image = rng.integers(0, 255, size=(32, 32, 3), dtype=np.uint8)
    resized_image = ops.image.resize(
        ops.convert_to_tensor([image]), size=(image_size, image_size)
    )
    print(f"resized_dtype={resized_image.dtype}")

    class Patches(layers.Layer):
        def __init__(self, patch_size):
            super().__init__()
            self.patch_size = patch_size

        def call(self, images):
            input_shape = ops.shape(images)
            batch_size = input_shape[0]
            height = input_shape[1]
            width = input_shape[2]
            channels = input_shape[3]
            num_patches_h = height // self.patch_size
            num_patches_w = width // self.patch_size
            patches = keras.ops.image.extract_patches(images, size=self.patch_size)
            return ops.reshape(
                patches,
                (
                    batch_size,
                    num_patches_h * num_patches_w,
                    self.patch_size * self.patch_size * channels,
                ),
            )

    patches = Patches(patch_size)(resized_image)
    print(f"patches_shape={patches.shape}")
    print(f"patches_dtype={patches.dtype}")


if __name__ == "__main__":
    main()
