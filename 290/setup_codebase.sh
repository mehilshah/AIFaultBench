#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/pytorch-image-models codebase
git -C codebase checkout af354f6a671083624482df637c0252f0504e5e87
# then: bash setup_env.sh && bash run_repro.sh
