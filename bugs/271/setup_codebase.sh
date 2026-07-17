#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/DeepSpeed codebase
git -C codebase checkout ad026a1fd1239071f2afb0a9c07f04b3cd732e02
# then: bash setup_env.sh && bash run_repro.sh
