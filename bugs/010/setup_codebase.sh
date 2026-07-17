#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/models codebase
git -C codebase checkout 19ce8ecda0732e52d943ccdf540a5659d103c2fc
# then: bash setup_env.sh && bash run_repro.sh
