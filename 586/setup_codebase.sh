#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/DeepSpeed codebase
git -C codebase checkout e0a6bb510bf77f5f5b3907da2a76786abe74eef1
# then: bash setup_env.sh && bash run_repro.sh
