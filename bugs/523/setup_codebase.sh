#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/accelerate codebase
git -C codebase checkout 2f83b1afefae2c13f9be36419da9f39c283de07d
# then: bash setup_env.sh && bash run_repro.sh
