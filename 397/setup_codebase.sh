#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/pytorch-image-models codebase
git -C codebase checkout cebc007d66041fee4e468305065872ec1200bec2
# then: bash setup_env.sh && bash run_repro.sh
