#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/denoising-diffusion-pytorch codebase
git -C codebase checkout 840d3ffd3b64276250faec2ec612e13847f69894
# then: bash setup_env.sh && bash run_repro.sh
