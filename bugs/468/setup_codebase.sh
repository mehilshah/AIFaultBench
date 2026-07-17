#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/DeepSpeed codebase
git -C codebase checkout 15ad92b459c6c39b7c5527efe1e42080eb4ab99f
# then: bash setup_env.sh && bash run_repro.sh
