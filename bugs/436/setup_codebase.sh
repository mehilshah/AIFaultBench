#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Lightning-AI/pytorch-lightning codebase
git -C codebase checkout 6805188c711094339e76d81668a4037dd56f7c7a
# then: bash setup_env.sh && bash run_repro.sh
