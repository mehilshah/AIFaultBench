#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/pytorch-image-models codebase
git -C codebase checkout d1140c1a0f21cab390f01b32768745f56ac0e87a
# then: bash setup_env.sh && bash run_repro.sh
