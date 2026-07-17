#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/keras-team/keras-io codebase
git -C codebase checkout c36c0c95a73944e99452afe6d87c17bcc93c4e3a
# then: bash setup_env.sh && bash run_repro.sh
