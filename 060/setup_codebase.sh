#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/keras-team/keras-io codebase
git -C codebase checkout bd6963345e520ab8b2cbf5894645ab070514aae1
# then: bash setup_env.sh && bash run_repro.sh
