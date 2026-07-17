#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/sdv-dev/SDV codebase
git -C codebase checkout ad8e4e09bdd01338ea94a60cddd1f06c815273aa
# then: bash setup_env.sh && bash run_repro.sh
