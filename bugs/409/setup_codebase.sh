#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/DeepSpeed codebase
git -C codebase checkout a44fb58f134afc5399b29c154a5502e14272774c
# then: bash setup_env.sh && bash run_repro.sh
