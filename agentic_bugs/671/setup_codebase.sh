#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pydantic/pydantic-ai codebase
git -C codebase checkout 77f86fa06f5fdde847f782710c5964e41037f096
# then: bash setup_env.sh && bash run_repro.sh
