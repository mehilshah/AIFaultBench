#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/NVIDIA/DeepLearningExamples codebase
git -C codebase checkout 0e20ac8e84db2f879c4388b6bcaa11a93a0599a1
# then: bash setup_env.sh && bash run_repro.sh
