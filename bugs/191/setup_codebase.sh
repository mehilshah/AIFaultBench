#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/NVIDIA/apex codebase
git -C codebase checkout 59b80ee8df79cec125794949327f29913c328746
# then: bash setup_env.sh && bash run_repro.sh
