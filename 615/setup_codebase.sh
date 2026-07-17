#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout 8570c25a745da54ca647b8a70231112f063d1421
# then: bash setup_env.sh && bash run_repro.sh
