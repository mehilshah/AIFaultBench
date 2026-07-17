#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/denoising-diffusion-pytorch codebase
git -C codebase checkout 7558d3f59962a9287bd524c464b2edef0e6fae76
# then: bash setup_env.sh && bash run_repro.sh
