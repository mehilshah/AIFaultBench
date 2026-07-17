#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/InternLM/lmdeploy codebase
git -C codebase checkout 0da627e
# then: bash setup_env.sh && bash run_repro.sh
