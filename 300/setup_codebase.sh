#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/diffusers codebase
git -C codebase checkout 72eb60c2dad62e44777b5344f21705c6d47bf97f
# then: bash setup_env.sh && bash run_repro.sh
