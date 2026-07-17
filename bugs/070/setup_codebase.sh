#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/deepspeedai/DeepSpeedExamples codebase
git -C codebase checkout 476f600be931e77b1d819ff05cc78709608d5269
# then: bash setup_env.sh && bash run_repro.sh
