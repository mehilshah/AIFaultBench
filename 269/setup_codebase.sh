#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Lightning-AI/pytorch-lightning codebase
git -C codebase checkout eea74433ce552f962d3e345f138c5fa7de723638
# then: bash setup_env.sh && bash run_repro.sh
