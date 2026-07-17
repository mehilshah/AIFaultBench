#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Lightning-AI/pytorch-lightning codebase
git -C codebase checkout efb73287b6db1bc86d1eb94fde2378a3dfb87be1
# then: bash setup_env.sh && bash run_repro.sh
