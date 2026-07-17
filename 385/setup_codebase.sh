#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout 80381880145591e3546c9bbe850bcbe277d8bfa3
# then: bash setup_env.sh && bash run_repro.sh
