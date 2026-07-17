#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/NVIDIA/DeepLearningExamples codebase
git -C codebase checkout acecffe16f0358cc7247893cca00707d63e527e1
# then: bash setup_env.sh && bash run_repro.sh
