#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/NVIDIA/DeepLearningExamples codebase
git -C codebase checkout 35d8759cb8cf52f8c7d33900ef27fd0f16d6cff3
# then: bash setup_env.sh && bash run_repro.sh
