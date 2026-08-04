#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/clearml/clearml codebase
git -C codebase checkout 3094d57140be9814e29584a77a15e05ca90631ce
# then: bash setup_env.sh && bash run_repro.sh
