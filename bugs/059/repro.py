import tensorflow as tf
import keras_cv


def make_ground_truth(num_boxes: int):
    return {
        "boxes": tf.zeros((1, num_boxes, 4), dtype=tf.float32),
        "classes": tf.zeros((1, num_boxes), dtype=tf.float32),
    }


def make_predictions(num_boxes: int):
    return {
        "boxes": tf.zeros((1, num_boxes, 4), dtype=tf.float32),
        "classes": tf.zeros((1, num_boxes), dtype=tf.float32),
        "confidence": tf.ones((1, num_boxes), dtype=tf.float32),
    }


def main():
    print(f"tensorflow={tf.__version__}")
    print(f"keras_cv={keras_cv.__version__}")

    metric = keras_cv.metrics.BoxCOCOMetrics(
        bounding_box_format="xyxy",
        evaluate_freq=1e9,
    )

    metric.update_state(make_ground_truth(2), make_predictions(2))
    metric.update_state(make_ground_truth(1), make_predictions(1))

    print("Calling result(force=True)...")
    print(metric.result(force=True))


if __name__ == "__main__":
    main()
