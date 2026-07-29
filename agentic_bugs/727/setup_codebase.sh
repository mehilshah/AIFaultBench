#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/openai/openai-agents-python codebase
git -C codebase checkout da82b2cd663ee263b206ce65179c26b598d61f73
# then: bash setup_env.sh && bash run_repro.sh
