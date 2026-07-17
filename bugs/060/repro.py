import os
import sys
import traceback

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import tensorflow as tf
import keras_cv


def main():
    print(f"tensorflow={tf.__version__}")
    print(f"keras_cv={keras_cv.__version__}")

    rand_augment = keras_cv.layers.RandAugment(
        value_range=(0, 255),
        augmentations_per_image=3,
        magnitude=0.3,
        magnitude_stddev=0.2,
        rate=0.5,
    )

    def augment_fn(sample):
        return rand_augment(sample)

    train_ds = tf.data.Dataset.from_tensors(
        {
            "images": tf.zeros((160, 160, 3), dtype=tf.float32),
            "segmentation_masks": tf.zeros((160, 160, 1), dtype=tf.int64),
        }
    )

    augmented_train_ds = (
        train_ds.shuffle(2)
        .map(augment_fn, num_parallel_calls=tf.data.AUTOTUNE)
        .batch(1)
    )

    print("Triggering dataset trace...")
    try:
        next(iter(augmented_train_ds))
    except Exception as exc:
        print("REPRODUCED")
        print(f"{type(exc).__name__}: {exc}")
        raise

    print("No error raised.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(1)
