#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pydantic/pydantic-ai codebase
git -C codebase checkout e9ebd28626152401b9b485337ce6c1175dbbe681
# then: bash setup_env.sh && bash run_repro.sh
