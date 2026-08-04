#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/google/deepvariant codebase
git -C codebase checkout b4e87ce4fb84c415fc9ccbbcc96c380cd52b3b14
# then: bash setup_env.sh && bash run_repro.sh
