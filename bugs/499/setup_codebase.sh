#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Lightning-AI/pytorch-lightning codebase
git -C codebase checkout 92a54747aa40273b07a1c15a25a486bb4b37f13d
# then: bash setup_env.sh && bash run_repro.sh
