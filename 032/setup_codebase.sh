#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/NVIDIA/DeepLearningExamples codebase
git -C codebase checkout f613b7c0a8ff252dcbc8cc7747995334198844b3
# then: bash setup_env.sh && bash run_repro.sh
