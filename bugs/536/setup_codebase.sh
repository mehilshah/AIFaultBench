#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/vllm-project/vllm codebase
git -C codebase checkout 248d1fbb711b210784ab880593403d665a4731bd
# then: bash setup_env.sh && bash run_repro.sh
