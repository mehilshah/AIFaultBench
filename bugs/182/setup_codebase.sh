#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Lightning-AI/pytorch-lightning codebase
git -C codebase checkout 791753b1c3ed0e434ee097564caceea2d8bc76ea
# then: bash setup_env.sh && bash run_repro.sh
