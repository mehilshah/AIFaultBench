#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/pytorch-image-models codebase
git -C codebase checkout ea728f67fa26779f65e1cb9738ece458dbc86a42
# then: bash setup_env.sh && bash run_repro.sh
