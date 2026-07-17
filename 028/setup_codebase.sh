#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/examples codebase
git -C codebase checkout 6fc19c76b9f5550d8d3cb38284845ac7ed14223c
# then: bash setup_env.sh && bash run_repro.sh
