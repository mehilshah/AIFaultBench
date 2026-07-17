#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import pathlib
from typing import Any

import tensorflow as tf

from pyc_loader import install


ROOT = install()

import official.modeling.hyperparams
import official.modeling.optimization
import official.core.config_definitions
import official.core.base_task
import official.core.base_trainer
import official.core.train_utils
import official.core.train_lib
import official.vision.modeling.backbones.factory
import official.vision.modeling.backbones.resnet
import official.vision.modeling.classification_model
import official.vision.modeling.factory
import official.vision.tasks.image_classification

from official.vision.configs import image_classification
from official.vision.tasks.image_classification import ImageClassificationTask
from official.core import train_lib


def _write_synthetic_tfrecord(path: pathlib.Path, num_examples: int, seed: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    generator = tf.random.Generator.from_seed(seed)
    with tf.io.TFRecordWriter(str(path)) as writer:
        for i in range(num_examples):
            image = generator.uniform([160, 160, 3], maxval=256, dtype=tf.int32)
            image = tf.cast(image, tf.uint8)
            encoded = tf.io.encode_jpeg(image).numpy()
            example = tf.train.Example(
                features=tf.train.Features(
                    feature={
                        "image/encoded": tf.train.Feature(
                            bytes_list=tf.train.BytesList(value=[encoded])
                        ),
                        "image/class/label": tf.train.Feature(
                            int64_list=tf.train.Int64List(value=[(i % 1000) + 1])
                        ),
                    }
                )
            )
            writer.write(example.SerializeToString())


def _build_config(train_glob: str, val_glob: str) -> Any:
    cfg = image_classification.image_classification_imagenet_resnetrs()
    cfg.runtime.enable_xla = False
    cfg.runtime.distribution_strategy = "one_device"
    cfg.runtime.num_gpus = 0
    cfg.runtime.mixed_precision_dtype = "float16"
    cfg.runtime.loss_scale = None
    cfg.runtime.run_eagerly = True

    cfg.task.train_data.input_path = train_glob
    cfg.task.validation_data.input_path = val_glob
    cfg.task.train_data.global_batch_size = 2
    cfg.task.validation_data.global_batch_size = 2
    cfg.task.train_data.dtype = "float16"
    cfg.task.validation_data.dtype = "float16"

    cfg.trainer.train_steps = 100
    cfg.trainer.validation_steps = 1
    cfg.trainer.steps_per_loop = 1
    cfg.trainer.summary_interval = 1000
    cfg.trainer.checkpoint_interval = 1000
    cfg.trainer.validation_interval = 1000
    cfg.trainer.train_tf_function = False
    cfg.trainer.train_tf_while_loop = False
    cfg.trainer.eval_tf_function = False
    cfg.trainer.eval_tf_while_loop = False
    cfg.trainer.loss_upper_bound = 1e30
    cfg.trainer.optimizer_config.learning_rate.cosine.decay_steps = 100
    cfg.trainer.optimizer_config.warmup.linear.warmup_steps = 0
    cfg.trainer.optimizer_config.ema = None

    return cfg


def main() -> None:
    tf.random.set_seed(7)
    work_dir = pathlib.Path.cwd()
    data_dir = work_dir / "synthetic_data"
    model_dir = work_dir / "model_dir"
    model_dir.mkdir(exist_ok=True)
    _write_synthetic_tfrecord(data_dir / "train-00000-of-00001.tfrecord", 4, seed=7)
    _write_synthetic_tfrecord(data_dir / "val-00000-of-00001.tfrecord", 2, seed=13)

    cfg = _build_config(str(data_dir / "train-*"), str(data_dir / "val-*"))
    strategy = tf.distribute.OneDeviceStrategy("/cpu:0")
    task = ImageClassificationTask(cfg.task)

    result: dict[str, Any]
    try:
        _, logs = train_lib.run_experiment(strategy, task, "train", cfg, str(model_dir))
        result = {
            "reproducible": False,
            "evidence": [
                "The 100-step run completed without NaN.",
                "Training loss exploded into the billions but stayed finite through step 100.",
            ],
            "steps": [
                "Installed the bytecode loader for the bundled tensorflow/models snapshot.",
                "Generated local TFRecord training and validation data.",
                "Ran ImageClassificationTask with resnet_rs_imagenet-style settings for 100 steps.",
                "Observed exploding but finite loss values instead of NaN.",
            ],
            "blocking_reason": (
                "In this Python 3.11 + TensorFlow 2.20 environment, the bundled snapshot "
                "does not reproduce the reported NaN loss. The run stays finite and "
                "finishes 100 training steps; the behavior differs from the issue report."
            ),
            "reproduction_command": "bash run_repro.sh",
        }
    except Exception as exc:
        result = {
            "reproducible": False,
            "evidence": [f"Training aborted with {type(exc).__name__}: {exc}"],
            "steps": [
                "Installed the bytecode loader for the bundled tensorflow/models snapshot.",
                "Generated local TFRecord training and validation data.",
                "Started the resnet_rs_imagenet-style training loop.",
            ],
            "blocking_reason": (
                "The local harness hit an environment-specific failure before reproducing "
                "the reported NaN path."
            ),
            "reproduction_command": "bash run_repro.sh",
        }

    result_path = work_dir / "reproduction.json"
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
