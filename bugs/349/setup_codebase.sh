#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/accelerate codebase
git -C codebase checkout 5060574827ffcf1055179896cbb4f150caa3aec5
# then: bash setup_env.sh && bash run_repro.sh
