#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout a1a107003252a3ab2a0830702d21b7f46caff6d7
# then: bash setup_env.sh && bash run_repro.sh
