#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/denoising-diffusion-pytorch codebase
git -C codebase checkout 242e4b63dad7d5d9d0bf4f465f861f98dfba918d
# then: bash setup_env.sh && bash run_repro.sh
