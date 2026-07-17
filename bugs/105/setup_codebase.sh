#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/vector-quantize-pytorch codebase
git -C codebase checkout 133f7386df6cf83345bb7cddca741d0364753af1
# then: bash setup_env.sh && bash run_repro.sh
