#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/peft codebase
git -C codebase checkout 41c274ecac6247a63e3b10f8536904f3ead82213
# then: bash setup_env.sh && bash run_repro.sh
