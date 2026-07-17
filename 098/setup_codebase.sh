#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/denoising-diffusion-pytorch codebase
git -C codebase checkout fd5e62f7054f65dacd211713d29cc819b9f3378d
# then: bash setup_env.sh && bash run_repro.sh
