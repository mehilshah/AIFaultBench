#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/deepspeedai/DeepSpeedExamples codebase
git -C codebase checkout df7119ed264bfac747969f9bb5bed8a61aed5e5d
# then: bash setup_env.sh && bash run_repro.sh
