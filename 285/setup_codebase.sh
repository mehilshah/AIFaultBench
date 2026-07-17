#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Lightning-AI/pytorch-lightning codebase
git -C codebase checkout 4819088b0c6838f0d878b30050d59003305924b8
# then: bash setup_env.sh && bash run_repro.sh
