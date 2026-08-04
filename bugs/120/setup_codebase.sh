#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/DLR-RM/stable-baselines3 codebase
git -C codebase checkout ba77dd7c6180c0ec9a47dfa98291c2103e6750df
# then: bash setup_env.sh && bash run_repro.sh
