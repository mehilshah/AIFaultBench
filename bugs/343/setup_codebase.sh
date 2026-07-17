#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/sdv-dev/SDV codebase
git -C codebase checkout db5bcb22a86ca2a1f790f531f0df4a7bd6cc737d
# then: bash setup_env.sh && bash run_repro.sh
