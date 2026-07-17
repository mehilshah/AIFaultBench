#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Lightning-AI/pytorch-lightning codebase
git -C codebase checkout 7d2de87084573e4f75aa83189d0fb43c463120e8
# then: bash setup_env.sh && bash run_repro.sh
