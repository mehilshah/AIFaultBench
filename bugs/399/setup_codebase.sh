#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout f54a7c70c6ddc342867ac113bf12b908404df79c
# then: bash setup_env.sh && bash run_repro.sh
