#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/tutorials codebase
git -C codebase checkout 86b1c6297381e3b46560db14f9f1fb6fe267deec
# then: bash setup_env.sh && bash run_repro.sh
