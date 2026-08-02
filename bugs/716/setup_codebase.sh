#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/SWE-agent/SWE-agent codebase
git -C codebase checkout aa4e8ea1611dad2220950cc5afb30aff17932b41
# then: bash setup_env.sh && bash run_repro.sh
