#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/facebookresearch/fairseq codebase
git -C codebase checkout 4fe8583396191c22011350248119db98ec1b5cb8
# then: bash setup_env.sh && bash run_repro.sh
