import importlib.util
import tempfile
from pathlib import Path

import numpy as np
import torch as th
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator


ROOT = Path(__file__).resolve().parent
LOGGER_PATH = ROOT / "codebase" / "stable_baselines3" / "common" / "logger.py"


def load_logger_module():
    spec = importlib.util.spec_from_file_location("sb3_logger", LOGGER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main():
    logger_mod = load_logger_module()
    folder = Path(tempfile.mkdtemp(prefix="sb3_tb_bug_"))

    logger = logger_mod.Logger(
        folder=str(folder),
        output_formats=[logger_mod.TensorBoardOutputFormat(folder=str(folder))],
    )

    np_value = np.random.rand(5)
    th_value = th.rand(5)

    logger.record("numpy", np_value)
    logger.record("torch", th_value)
    logger.dump(0)

    acc = EventAccumulator(str(folder))
    acc.Reload()

    histogram_keys = set(acc.histograms.Keys())
    compressed_histogram_keys = set(acc.compressed_histograms.Keys())
    observed_keys = histogram_keys | compressed_histogram_keys

    print(f"tensorboard_dir={folder}")
    print(f"histograms={sorted(histogram_keys)}")
    print(f"compressed_histograms={sorted(compressed_histogram_keys)}")
    print(f"observed_histograms={sorted(observed_keys)}")

    assert "torch" in observed_keys, "torch tensor was not logged as a histogram"
    assert "numpy" in observed_keys, "np.ndarray was not logged as a histogram"


if __name__ == "__main__":
    main()
