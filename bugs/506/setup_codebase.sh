#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/diffusers codebase
git -C codebase checkout 01969142b55379991fee07608c9e7e8f80afced0
# then: bash setup_env.sh && bash run_repro.sh
