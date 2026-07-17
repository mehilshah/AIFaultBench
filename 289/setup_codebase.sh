#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/peft codebase
git -C codebase checkout 7dcdf7b311007b90ab085bb5dcd69f10ff32a30c
# then: bash setup_env.sh && bash run_repro.sh
