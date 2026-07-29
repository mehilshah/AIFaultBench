#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pydantic/pydantic-ai codebase
git -C codebase checkout e1691ea0247bb8ca09adc532e8b2f04eebc9ffe9
# then: bash setup_env.sh && bash run_repro.sh
