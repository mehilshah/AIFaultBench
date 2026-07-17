#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Lightning-AI/pytorch-lightning codebase
git -C codebase checkout c05cadbe5be3bfa8bacbd9d7e912fa2e456413ff
# then: bash setup_env.sh && bash run_repro.sh
