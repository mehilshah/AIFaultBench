#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/datasets codebase
git -C codebase checkout d5401a0d5c0ca6405ca5ba46b800a615b5ad372a
# then: bash setup_env.sh && bash run_repro.sh
