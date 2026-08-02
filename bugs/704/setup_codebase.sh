#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pydantic/pydantic-ai codebase
git -C codebase checkout a84f2b31d14de3572d51676ea1839c031d85362a
# then: bash setup_env.sh && bash run_repro.sh
