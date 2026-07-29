#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/camel-ai/camel codebase
git -C codebase checkout ff7e2d6d32365253e9d4184663fb0f95533d4731
# then: bash setup_env.sh && bash run_repro.sh
