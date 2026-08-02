#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pydantic/pydantic-ai codebase
git -C codebase checkout 88fb4e34eb24bb39d08a900bfe5f631d7df49484
# then: bash setup_env.sh && bash run_repro.sh
