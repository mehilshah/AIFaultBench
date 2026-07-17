import tensorflow as tf
from keras_cv.metrics import BoxCOCOMetrics


def make_batch(num_boxes: int):
    y_true = {
        "boxes": tf.zeros((4, num_boxes, 4), dtype=tf.float32),
        "classes": tf.zeros((4, num_boxes), dtype=tf.int32),
    }
    y_pred = {
        "boxes": tf.zeros((4, num_boxes, 4), dtype=tf.float32),
        "classes": tf.zeros((4, num_boxes), dtype=tf.int32),
        "confidence": tf.ones((4, num_boxes), dtype=tf.float32),
    }
    return y_true, y_pred


def main():
    print("tensorflow:", tf.__version__)
    print("keras-cv BoxCOCOMetrics concat repro")

    metric = BoxCOCOMetrics(
        bounding_box_format="xyxy",
        evaluate_freq=10**9,
    )

    for num_boxes in (2, 1):
        y_true, y_pred = make_batch(num_boxes)
        print(
            f"update_state batch with boxes shape={y_true['boxes'].shape}, "
            f"classes shape={y_true['classes'].shape}"
        )
        metric.update_state(y_true, y_pred)

    print("calling result(force=True)")
    metric.result(force=True)


if __name__ == "__main__":
    main()
