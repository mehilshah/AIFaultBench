#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout e82a69f5af94cc936c4b872fd2ed499ed33b4f8e
# then: bash setup_env.sh && bash run_repro.sh
