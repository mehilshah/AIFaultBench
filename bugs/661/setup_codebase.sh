#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/crewAIInc/crewAI codebase
git -C codebase checkout b0e2fda105c2e0c05c7abb1f53800443ffd582ea
# then: bash setup_env.sh && bash run_repro.sh
