#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/diffusers codebase
git -C codebase checkout 784fa62652fb2719d415830f918fc32a49ecc7a1
# then: bash setup_env.sh && bash run_repro.sh
