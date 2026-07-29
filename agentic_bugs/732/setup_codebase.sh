#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/mem0ai/mem0 codebase
git -C codebase checkout 17836748d7afe0521516c6a73c6a256680f05527
# then: bash setup_env.sh && bash run_repro.sh
