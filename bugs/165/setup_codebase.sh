#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/kornia/kornia codebase
git -C codebase checkout 58a6a4725229d8556061318c6d88194b077e60ed
# then: bash setup_env.sh && bash run_repro.sh
