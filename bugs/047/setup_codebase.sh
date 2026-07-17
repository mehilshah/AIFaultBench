#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/facebookresearch/fairseq codebase
git -C codebase checkout 25c20e6a5e781e4ef05e23642f21c091ba64872e
# then: bash setup_env.sh && bash run_repro.sh
