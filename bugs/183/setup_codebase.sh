#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/linkedin/Liger-Kernel codebase
git -C codebase checkout ac5667471e24434c378781c5400b19d595d05fd8
# then: bash setup_env.sh && bash run_repro.sh
