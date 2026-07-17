#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/vector-quantize-pytorch codebase
git -C codebase checkout 59a30b68a83be710638184764c025b54693c82cc
# then: bash setup_env.sh && bash run_repro.sh
