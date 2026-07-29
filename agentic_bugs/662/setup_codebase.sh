#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/crewAIInc/crewAI codebase
git -C codebase checkout 1c90d574abb9f28dd09de8ded437bcad19fa97dc
# then: bash setup_env.sh && bash run_repro.sh
