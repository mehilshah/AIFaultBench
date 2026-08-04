#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Lightning-AI/pytorch-lightning codebase
git -C codebase checkout 1f5add327fd88fe288a2f889d720e5d5e06bd7d2
# then: bash setup_env.sh && bash run_repro.sh
