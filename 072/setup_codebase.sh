#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/deepspeedai/DeepSpeedExamples codebase
git -C codebase checkout 957ae3141946daf9a6bc5731e261032a13a82f05
# then: bash setup_env.sh && bash run_repro.sh
