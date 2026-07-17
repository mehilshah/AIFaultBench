#!/usr/bin/env python3
"""Static reproduction harness for TF Models issue #11042.

This bug report is about multi-worker ImageNet throughput not scaling on GPUs.
The standardized folder does not contain a runnable 2-node GPU cluster, so this
script validates the repo's relevant code paths and records why a functional
reproduction is not possible locally.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BUG_REPORT = ROOT / "bug_report.txt"
TRAINER = ROOT / "codebase/official/legacy/image_classification/classifier_trainer.py"
DATASET_FACTORY = ROOT / "codebase/official/legacy/image_classification/dataset_factory.py"
DIST_UTILS = ROOT / "codebase/official/common/distribute_utils.py"
GPU_YAML = ROOT / "codebase/official/legacy/image_classification/configs/examples/resnet/imagenet/gpu.yaml"


def read_text(path: Path) -> str:
  return path.read_text(encoding="utf-8")


def excerpt(path: Path, needle: str, radius: int = 2) -> str:
  lines = read_text(path).splitlines()
  for idx, line in enumerate(lines):
    if needle in line:
      start = max(0, idx - radius)
      end = min(len(lines), idx + radius + 1)
      snippet = []
      for lineno in range(start, end):
        snippet.append(f"{lineno + 1}: {lines[lineno]}")
      return "\n".join(snippet)
  return "<needle not found>"


def parse_distribution_strategy(gpu_yaml: str) -> str:
  match = re.search(r"distribution_strategy:\s*['\"]?([^'\"]+)['\"]?", gpu_yaml)
  return match.group(1) if match else "<missing>"


def main() -> None:
  bug_report = read_text(BUG_REPORT)
  trainer = read_text(TRAINER)
  dataset_factory = read_text(DATASET_FACTORY)
  dist_utils = read_text(DIST_UTILS)
  gpu_yaml = read_text(GPU_YAML)

  report = {
      "issue_title": "Tensorflow2 Multi worker mirrored strategy is not scaling for GPUS",
      "checked_in_gpu_yaml_distribution_strategy": parse_distribution_strategy(
          gpu_yaml
      ),
      "bug_report_mentions_multi_worker": "multi_worker_mirrored" in bug_report,
      "trainer_configures_cluster": "configure_cluster(" in trainer,
      "trainer_uses_multi_worker_strategy":
          "MultiWorkerMirroredStrategy" in dist_utils,
      "dataset_builder_shards_multi_input_pipelines":
          "dataset.shard(self.input_context.num_input_pipelines" in dataset_factory,
      "dataset_builder_uses_distribute_datasets_from_function":
          "distribute_datasets_from_function" in dataset_factory,
  }

  print(json.dumps(report, indent=2, sort_keys=True))
  print()
  print("Evidence: classifier_trainer.py cluster setup")
  print(excerpt(TRAINER, "configure_cluster(", radius=2))
  print()
  print("Evidence: distribute_utils.py multi-worker strategy selection")
  print(excerpt(DIST_UTILS, 'if distribution_strategy == "multi_worker_mirrored":', radius=4))
  print()
  print("Evidence: dataset_factory.py input pipeline sharding")
  print(excerpt(DATASET_FACTORY, "dataset.shard(self.input_context.num_input_pipelines", radius=4))
  print()
  print("Evidence: checked-in gpu.yaml")
  print(excerpt(GPU_YAML, "distribution_strategy", radius=2))
  print()
  print(
      "Verdict: not reproducible here. The report is about multi-node GPU "
      "throughput, but this workspace has no GPU cluster to benchmark, and the "
      "checked-in resnet gpu.yaml is single-worker mirrored rather than the "
      "multi_worker_mirrored configuration described in the report."
  )


if __name__ == "__main__":
  main()
