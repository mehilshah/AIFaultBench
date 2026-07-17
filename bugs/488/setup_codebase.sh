#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/vllm-project/vllm codebase
git -C codebase checkout 3406e8f83dad17d044d38853f75270c7b636bb95
# then: bash setup_env.sh && bash run_repro.sh
