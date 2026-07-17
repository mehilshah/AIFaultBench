#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Lightning-AI/pytorch-lightning codebase
git -C codebase checkout 35e56ef93582c60c8ec5ca2bf1025e7c414d6bb6
# then: bash setup_env.sh && bash run_repro.sh
