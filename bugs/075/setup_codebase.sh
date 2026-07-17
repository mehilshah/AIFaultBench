#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/deepspeedai/DeepSpeedExamples codebase
git -C codebase checkout ff9a0234cf22dd9af03c5c7aa8037fb9143adca6
# then: bash setup_env.sh && bash run_repro.sh
