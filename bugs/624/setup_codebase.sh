#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/accelerate codebase
git -C codebase checkout e9d15e59732fab5a123f61ec7ccb6dd41e207542
# then: bash setup_env.sh && bash run_repro.sh
