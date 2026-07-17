#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/deepspeedai/DeepSpeedExamples codebase
git -C codebase checkout f73a6ed635659f03ac583a1d914ea07a2cbeab99
# then: bash setup_env.sh && bash run_repro.sh
