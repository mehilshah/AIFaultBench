#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/sdv-dev/SDV codebase
git -C codebase checkout 1114b575eba1ddd2b02446e6dec42e40909d86fc
# then: bash setup_env.sh && bash run_repro.sh
