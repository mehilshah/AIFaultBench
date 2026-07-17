#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/transformers codebase
git -C codebase checkout 9b6af5d77de78f0a57a098b2809009ad6ec0cfe3
# then: bash setup_env.sh && bash run_repro.sh
