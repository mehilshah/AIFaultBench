import os

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import tensorflow as tf
import keras_cv


def build_dataset():
    images = tf.zeros((2, 512, 512, 3), dtype=tf.float32)
    boxes = tf.zeros((2, 0, 4), dtype=tf.float32)
    classes = tf.zeros((2, 0), dtype=tf.float32)

    dataset = tf.data.Dataset.from_tensor_slices(
        {
            "images": images,
            "bounding_boxes": {"boxes": boxes, "classes": classes},
        }
    ).batch(2)

    @tf.autograph.experimental.do_not_convert
    def dict_to_tuple(inputs):
        return inputs["images"], inputs["bounding_boxes"]

    return dataset.map(dict_to_tuple)


def main():
    print(f"tensorflow={tf.__version__}")
    print(f"keras_cv={keras_cv.__version__}")

    dataset = build_dataset()

    backbone = keras_cv.models.ResNetBackbone.from_preset("resnet50")
    model = keras_cv.models.RetinaNet(
        backbone=backbone,
        num_classes=1,
        bounding_box_format="xywh",
    )
    model.compile(
        classification_loss="focal",
        box_loss="smoothl1",
        optimizer="sgd",
    )

    print("starting fit")
    model.fit(dataset, epochs=1, steps_per_epoch=1)


if __name__ == "__main__":
    main()
