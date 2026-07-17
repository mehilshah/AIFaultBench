#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/NVIDIA/DeepLearningExamples codebase
git -C codebase checkout 729963dd47e7c8bd462ad10bfac7a7b0b604e6dd
# then: bash setup_env.sh && bash run_repro.sh
