#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/jupyter/docker-stacks codebase
git -C codebase checkout 0098788
# then: bash setup_env.sh && bash run_repro.sh
