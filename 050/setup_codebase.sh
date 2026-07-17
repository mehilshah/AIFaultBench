#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/keras-team/keras-io codebase
git -C codebase checkout 3e3467de2b61a5af6291dcf860089885614d58ad
# then: bash setup_env.sh && bash run_repro.sh
