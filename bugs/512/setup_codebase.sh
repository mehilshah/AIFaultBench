#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Lightning-AI/pytorch-lightning codebase
git -C codebase checkout 8d86b2417d56703d5cc4f0da76acc71717d1dab7
# then: bash setup_env.sh && bash run_repro.sh
