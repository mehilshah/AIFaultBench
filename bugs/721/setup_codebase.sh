#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/browser-use/browser-use codebase
git -C codebase checkout 859cb970631043c7d484ea9a778ad4b9f65383b3
# then: bash setup_env.sh && bash run_repro.sh
