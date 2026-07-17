#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout 996387f029820bf7bd81b333154988388344ced8
# then: bash setup_env.sh && bash run_repro.sh
