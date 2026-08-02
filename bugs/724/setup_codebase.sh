#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/crewAIInc/crewAI codebase
git -C codebase checkout cb46a1c4babef8c51db6499d7a81f2c36b01bdef
# then: bash setup_env.sh && bash run_repro.sh
