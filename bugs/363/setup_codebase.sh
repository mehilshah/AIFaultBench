#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Lightning-AI/pytorch-lightning codebase
git -C codebase checkout 0e20e15f2376f4f356470b08875639a945c43334
# then: bash setup_env.sh && bash run_repro.sh
