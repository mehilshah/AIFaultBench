#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/crewAIInc/crewAI codebase
git -C codebase checkout 0b120fac902363670976a036aa72693ba0018aa7
# then: bash setup_env.sh && bash run_repro.sh
