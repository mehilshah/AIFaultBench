#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/keras-team/keras-io codebase
git -C codebase checkout b124d091b3ee87b6ae6b10ed2707be18e647c81d
# then: bash setup_env.sh && bash run_repro.sh
