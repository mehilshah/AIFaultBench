#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Lightning-AI/pytorch-lightning codebase
git -C codebase checkout 8e805f9268043c9aa8f0d70800be537b56a93c19
# then: bash setup_env.sh && bash run_repro.sh
