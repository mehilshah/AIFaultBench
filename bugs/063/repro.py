import tensorflow as tf
import keras_cv


HEIGHT = 160
WIDTH = 160
NUM_CLASSES = 3
ROTATION_FACTOR = (-0.2, 0.2)


def make_sample(_):
    return {
        "images": tf.zeros((HEIGHT, WIDTH, 3), dtype=tf.float32),
        "segmentation_masks": tf.zeros((HEIGHT, WIDTH, 1), dtype=tf.int64),
    }


def build_augment_fn():
    resize_fn = keras_cv.layers.Resizing(HEIGHT, WIDTH)
    return tf.keras.Sequential(
        [
            resize_fn,
            keras_cv.layers.RandomFlip(),
            keras_cv.layers.RandomRotation(
                factor=ROTATION_FACTOR,
                segmentation_classes=NUM_CLASSES,
            ),
            keras_cv.layers.RandAugment(
                value_range=(0, 1),
                geometric=False,
            ),
        ]
    )


def main():
    tf.random.set_seed(1337)
    print("tensorflow:", tf.__version__)
    print("keras_cv:", keras_cv.__version__)
    augment_fn = build_augment_fn()

    dataset = (
        tf.data.Dataset.range(4)
        .map(make_sample, num_parallel_calls=tf.data.AUTOTUNE)
        .shuffle(4)
        .map(augment_fn, num_parallel_calls=tf.data.AUTOTUNE)
        .batch(2)
    )

    for batch in dataset.take(1):
        print({k: (v.dtype.name, tuple(v.shape)) for k, v in batch.items()})


if __name__ == "__main__":
    main()
