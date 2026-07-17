#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout 1ed0d1e40f590420a123006affb958b4c02b0b8c
# then: bash setup_env.sh && bash run_repro.sh
