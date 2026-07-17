#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/facebookresearch/fairseq codebase
git -C codebase checkout 100cd91db19bb27277a06a25eb4154c805b10189
# then: bash setup_env.sh && bash run_repro.sh
