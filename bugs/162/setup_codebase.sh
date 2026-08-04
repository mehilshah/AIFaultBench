#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/jupyter/docker-stacks codebase
git -C codebase checkout 00987883e58d139b5ed01f803f95e639c59bf340
# then: bash setup_env.sh && bash run_repro.sh
