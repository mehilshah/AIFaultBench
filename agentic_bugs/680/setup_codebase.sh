#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/camel-ai/camel codebase
git -C codebase checkout b7a2fda98db44d7b3feeda9259ef09ae0b0de8b5
# then: bash setup_env.sh && bash run_repro.sh
