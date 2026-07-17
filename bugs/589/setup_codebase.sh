#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout 7e0968aa621c0b67313b3f5db09d931baf8a1b3b
# then: bash setup_env.sh && bash run_repro.sh
