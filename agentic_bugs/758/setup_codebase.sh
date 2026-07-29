#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/smolagents codebase
git -C codebase checkout cb5ba00589be66d42bec009313e544384220ada9
# then: bash setup_env.sh && bash run_repro.sh
