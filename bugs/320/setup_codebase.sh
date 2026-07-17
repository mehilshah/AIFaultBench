#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/vllm-project/vllm codebase
git -C codebase checkout e5588e49bc2642670116664a7fc4096e27adb179
# then: bash setup_env.sh && bash run_repro.sh
