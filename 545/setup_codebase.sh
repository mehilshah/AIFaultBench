#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Lightning-AI/pytorch-lightning codebase
git -C codebase checkout 79a39c04d37434f2234d9b518a145854d7c1e642
# then: bash setup_env.sh && bash run_repro.sh
