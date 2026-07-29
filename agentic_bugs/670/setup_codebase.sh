#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pydantic/pydantic-ai codebase
git -C codebase checkout ab79636233fd3e4bb386306994da09ba53dd5654
# then: bash setup_env.sh && bash run_repro.sh
