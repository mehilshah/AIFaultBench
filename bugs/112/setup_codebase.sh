#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/albumentations-team/albumentations codebase
git -C codebase checkout 218d663bf80816a588fe8a922f5e79c8c0353587
# then: bash setup_env.sh && bash run_repro.sh
